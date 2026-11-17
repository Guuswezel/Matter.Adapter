require "yaml"

root = File.expand_path("../examples/homeassistant", __dir__)
automations = YAML.load_file(File.join(root, "automations.yaml"))
scripts = YAML.load_file(File.join(root, "scripts.yaml"))
raise "Duplicate automation IDs" unless automations.map { |a| a.fetch("id") }.uniq.size == 3

# Evaluate the actual YAML branches at schedule boundaries, without controlling devices.
def matches?(condition, clock, sunset)
  case condition.fetch("condition")
  when "time"
    clock >= condition.fetch("after", "00:00:00") && clock < condition.fetch("before", "24:00:00")
  when "sun"
    clock >= sunset
  when "state"
    raise "Unexpected state condition" unless condition["entity_id"] == "sun.sun"
    above = clock >= "07:00:00" && clock < sunset
    condition["state"] == (above ? "above_horizon" : "below_horizon")
  else
    raise "Unexpected condition"
  end
end

def actions_at(actions, clock, sunset)
  actions.flat_map do |step|
    if step["choose"]
      branch = step["choose"].find { |b| b.fetch("conditions").all? { |c| matches?(c, clock, sunset) } }
      actions_at(branch ? branch.fetch("sequence") : step.fetch("default"), clock, sunset)
    elsif step["if"]
      step["if"].all? { |c| matches?(c, clock, sunset) } ? actions_at(step.fetch("then"), clock, sunset) : []
    else
      [step]
    end
  end
end

by_id = automations.to_h { |a| [a.fetch("id"), a] }
tests = [
  ["aquarium_luft_daily_schedule", "16:59:59", "18:00:00", "switch.turn_off"],
  ["aquarium_luft_daily_schedule", "17:00:00", "18:00:00", "switch.turn_on"],
  ["aquarium_luft_daily_schedule", "17:14:59", "18:00:00", "switch.turn_on"],
  ["aquarium_luft_daily_schedule", "17:15:00", "18:00:00", "switch.turn_off"],
  ["aquarium_light_sun_schedule", "07:00:00", "18:00:00", "switch.turn_on"],
  ["aquarium_light_sun_schedule", "18:00:00", "18:00:00", "switch.turn_off"],
  ["weihnachts_stern_evening_schedule", "05:00:00", "18:00:00", "light.turn_off"],
  ["weihnachts_stern_evening_schedule", "18:00:00", "18:00:00", "light.turn_on"],
  ["weihnachts_stern_evening_schedule", "19:59:59", "18:00:00", "light.turn_on"],
  ["weihnachts_stern_evening_schedule", "20:00:00", "18:00:00", "script.turn_on"],
  ["weihnachts_stern_evening_schedule", "20:00:00", "20:15:00", "light.turn_off"],
  ["weihnachts_stern_evening_schedule", "20:15:00", "20:15:00", "script.turn_on"],
  ["weihnachts_stern_evening_schedule", "20:29:59", "18:00:00", "script.turn_on"],
  ["weihnachts_stern_evening_schedule", "20:30:00", "18:00:00", "light.turn_on"],
  ["weihnachts_stern_evening_schedule", "21:30:00", "21:30:00", "light.turn_on"],
  ["weihnachts_stern_evening_schedule", "23:00:00", "18:00:00", "light.turn_off"]
]
tests.each do |id, clock, sunset, expected|
  steps = actions_at(by_id.fetch(id).fetch("actions"), clock, sunset)
  raise "Wrong schedule at #{id} #{clock}" unless steps.last.fetch("action") == expected
  if id == "weihnachts_stern_evening_schedule"
    raise "Show not cancelled before schedule change" unless steps.first["action"] == "script.turn_off"
    steps.select { |s| s["action"] == "light.turn_on" }.each do |step|
      raise "Normal star colour must be 2400 K" unless step.dig("data", "color_temp_kelvin") == 2400
    end
  end
end

show = scripts.fetch("weihnachts_stern_light_show")
raise "Show must start at 20:00" unless show["sequence"].first["after"] == "20:00:00"
raise "Show must stop at 20:30" unless show["sequence"].first["before"] == "20:30:00"
puts "#{tests.size} schedule boundary/restart scenarios and 2400 K normal-state checks passed"
