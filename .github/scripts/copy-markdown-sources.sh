#!/usr/bin/env bash

set -euo pipefail

bundle exec ruby <<'RUBY'
require "fileutils"
require "jekyll"
require "pathname"

root = Dir.pwd

def normalise_output_path(url)
  path = url.sub(%r{\A/}, "")
  path = path.sub(%r{/index\z}, "")
  path.sub(%r{/\z}, "")
end

site = Jekyll::Site.new(
  Jekyll.configuration(
    "source" => root,
    "destination" => File.join(root, "_site"),
    "config" => "_config.yml"
  )
)

site.read

site.posts.docs.each do |doc|
  next unless File.extname(doc.path) == ".md"

  output_path = normalise_output_path(doc.url)
  next if output_path.empty?

  dest = File.join(site.dest, "#{output_path}.md")
  FileUtils.mkdir_p(File.dirname(dest))
  FileUtils.cp(doc.path, dest)

  source_path = Pathname.new(doc.path).relative_path_from(Pathname.new(root)).to_s
  dest_path = Pathname.new(dest).relative_path_from(Pathname.new(root)).to_s
  # puts "Copied #{source_path} -> #{dest_path}"
end
RUBY
