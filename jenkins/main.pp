exec { 'yum update':
  command => '/usr/bin/yum update'
}

exec { 'epel release':
  require => Exec['yum update'],
  command => '/usr/bin/yum install epel-release -y'
}

package { 'net-tools':
  require => Exec['yum update'],
  ensure => installed,
}

package { 'ufw':
  require => Exec['epel release'],
  ensure => installed,
}

exec { 'allow22':
  require => Package['ufw'],
  command => 'ufw allow 22'
  user => root
}

exec { 'allow80':
  require => Package['ufw'],
  command => 'ufw allow 80'
  user => root
}

exec { 'allow443':
  require => Package['ufw'],
  command => 'ufw allow 443'
  user => root
}

service { 'network':
  ensure => running,
}

exec { 'root login off':
  command => 'sed -i "s|#PermitRootLogin yes|PermitRootLogin no|g" /etc/ssh/sshd_config'
  require => File['/etc/ssh/sshd_config']
  user => root
}

####
net-tools
openssh-server
sudo sed -i "s|#PermitRootLogin yes|PermitRootLogin no|g" /etc/ssh/sshd_config
sudo yum install epel-release -y
sudo yum install ufw
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
#PermitRootLogin yes