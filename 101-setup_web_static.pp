# Ensure nginx package is installed
package { 'nginx':
  ensure => installed,
}

# Ensure nginx service is running and enabled
service { 'nginx':
  ensure     => running,
  enable     => true,
  require    => Package['nginx'],
}

# Ensure a directory exists
file { '/data/web_static/releases/test':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => Package['nginx'],
}

file { '/data/web_static/shared':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => package['nginx'],
}

# create empty file
file { '/data/web_static/releases/test/index.html':
  ensure   => file,
  require  => package['nginx'],
}

# create symbolic link
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
}

#
