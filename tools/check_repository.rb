require "yaml"
require "pathname"

root = Pathname.new(File.expand_path("..", __dir__))
Dir.chdir(root) do
  files = `git ls-files --cached --others --exclude-standard`.lines.map(&:chomp).uniq
  raise "Not a Git repository" unless $?.success?
  files.grep(/\.(yaml|yml)$/).each { |path| YAML.load_file(path) }
  app = YAML.load_file("xiao_otbr_patch/config.yaml")
  raise "App slug must preserve existing local installations" unless app["slug"] == "xiao_otbr_patch"
  raise "Only ARM64 has a validated OpenOCD package" unless app["arch"] == ["aarch64"]
  raise "Keep unverified changes experimental" unless app["stage"] == "experimental"
  raise "OpenOCD requires USB access" unless app["usb"]
  raise "Wrong baudrate" unless app.dig("options", "baudrate") == "460800"
  raise "Wrong flow control" unless app.dig("options", "flow_control") == false
  raise "Missing repository name" unless YAML.load_file("repository.yaml")["name"]
  app.fetch("options").each_key { |key| raise "Missing schema: #{key}" unless app.fetch("schema").key?(key) }
  files.each do |path|
    raise "Private/generated artifact in repository: #{path}" if path.match?(%r{\A(private|vendor|\.cache|\.tools|\.arduino|haos)/|\.(bin|gbl|hex|pyc|db|tar|bz2)\z})
    next unless File.file?(path)
    content = File.binread(path)
    raise "Private key in #{path}" if content.match?(/-----BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----/)
    next unless path.end_with?(".md")
    content.scan(/\[[^\]]*\]\(([^\s)]+)\)/).flatten.each do |link|
      next if link.match?(%r{\A(?:https?:|mailto:|#)})
      target = File.expand_path(link.split("#").first, File.dirname(path))
      raise "Broken relative link in #{path}: #{link}" unless File.exist?(target)
    end
  end
  puts "Repository metadata, YAML, documentation links and private-artifact checks passed (#{files.size} files)"
end
