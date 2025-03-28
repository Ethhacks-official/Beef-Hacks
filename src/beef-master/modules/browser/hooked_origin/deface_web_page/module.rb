#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#
class Deface_web_page < BeEF::Core::Command
  def self.options
    @configuration = BeEF::Core::Configuration.instance
    proto = @configuration.beef_proto
    beef_host = @configuration.beef_host
    beef_port = @configuration.beef_port
    base_host = "#{proto}://#{beef_host}:#{beef_port}"

    favicon_uri = "#{base_host}/ui/media/images/favicon.ico"
    [
      { 'name' => 'deface_title', 'description' => 'Page Title', 'ui_label' => 'New Title', 'value' => 'BeEF - The Browser Exploitation Framework Project',
        'width' => '200px' },
      { 'name' => 'deface_favicon', 'description' => 'Shortcut Icon', 'ui_label' => 'New Favicon', 'value' => favicon_uri, 'width' => '200px' },
      { 'name' => 'deface_content', 'description' => 'Your defacement content', 'ui_label' => 'Deface Content', 'type' => 'textarea', 'value' => 'BeEF!', 'width' => '400px',
        'height' => '100px' }
    ]
  end

  def post_execute
    content = {}
    content['Result'] = @datastore['result']
    save content
  end
end
