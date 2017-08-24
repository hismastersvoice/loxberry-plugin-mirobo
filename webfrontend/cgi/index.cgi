#!/usr/bin/perl

use File::HomeDir;
use CGI qw/:standard/;
use Config::Simple;
use Cwd 'abs_path';
use IO::Socket::INET;
use HTML::Entities;
use String::Escape qw( unquotemeta );
use warnings;
use strict;
no strict "refs"; # we need it for template system

my  $home = File::HomeDir->my_home;
my  $lang;
my  $installfolder;
my  $cfg;
my  $conf;
our $psubfolder;
our $template_title;
our $namef;
our $value;
our %query;
our $cache;
our $helptext;
our $language;	
our $select_language;
our $looptime;	
our $udp_port;	
our $debug;
our $select_debug;

our $r1_mi_robo_ip;
our $r1_mi_robo_token;	
our $r1_active;
our $r1_select_active;
our $r1_send_status;
our $r1_select_status;
our $r1_vti_error;
our $r1_vi_error_code;
our $r1_vti_state;
our $r1_vi_state_code;	
our $r1_vi_battery;
our $r1_vi_fanspeed;
our $r1_vi_area;
our $r1_vi_time;
our $r1_vi_dnd;	
our $r1_send_consumables;
our $r1_select_consumables;
our $r1_vi_mainbrush;
our $r1_vi_sidebrush;	
our $r1_vi_filter;
our $r1_vi_sensor;	
our $r1_send_cleaning_history;	
our $r1_select_chistory;
our $r1_vi_ch_time;
our $r1_vi_ch_count;
our $r1_vi_ch_area;

our $r2_mi_robo_ip;
our $r2_mi_robo_token;	
our $r2_active;
our $r2_select_active;
our $r2_send_status;
our $r2_select_status;
our $r2_vti_error;
our $r2_vi_error_code;
our $r2_vti_state;
our $r2_vi_state_code;	
our $r2_vi_battery;
our $r2_vi_fanspeed;
our $r2_vi_area;
our $r2_vi_time;
our $r2_vi_dnd;	
our $r2_send_consumables;
our $r2_select_consumables;
our $r2_vi_mainbrush;
our $r2_vi_sidebrush;	
our $r2_vi_filter;
our $r2_vi_sensor;
our $r2_send_cleaning_history;	
our $r2_select_chistory;
our $r2_vi_ch_time;
our $r2_vi_ch_count;
our $r2_vi_ch_area;

our $r3_mi_robo_ip;
our $r3_mi_robo_token;	
our $r3_active;
our $r3_select_active;
our $r3_send_status;
our $r3_select_status;
our $r3_vti_error;
our $r3_vi_error_code;
our $r3_vti_state;
our $r3_vi_state_code;	
our $r3_vi_battery;
our $r3_vi_fanspeed;
our $r3_vi_area;
our $r3_vi_time;
our $r3_vi_dnd;	
our $r3_send_consumables;
our $r3_select_consumables;
our $r3_vi_mainbrush;
our $r3_vi_sidebrush;	
our $r3_vi_filter;
our $r3_vi_sensor;
our $r3_send_cleaning_history;	
our $r3_select_chistory;
our $r3_vi_ch_time;
our $r3_vi_ch_count;
our $r3_vi_ch_area;

our $miniserver_ip;
our $miniserver_user;
our $miniserver_pass;
our $savedata;

# Read Settings
$cfg             = new Config::Simple("$home/config/system/general.cfg");
$miniserver_ip   = encode_entities($cfg->param('MINISERVER1.IPADDRESS'));
$miniserver_user = encode_entities($cfg->param('MINISERVER1.ADMIN'));
$miniserver_pass = encode_entities($cfg->param('MINISERVER1.PASS'));
$installfolder   = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");

print "Content-Type: text/html\n\n";

# Parse URL
foreach (split(/&/,$ENV{"QUERY_STRING"}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# Set parameters coming in - GET over POST

if ( !$query{'language'} )   { if ( param('language')  ) { $language = quotemeta(param('language'));         } 
else { $language = $language;  } } else { $language = quotemeta($query{'language'});   }
if ( !$query{'looptime'} )   { if ( param('looptime')  ) { $looptime = quotemeta(param('looptime'));         } 
else { $looptime = $looptime;  } } else { $looptime = quotemeta($query{'looptime'});   }
if ( !$query{'udp_port'} )   { if ( param('udp_port')  ) { $udp_port = quotemeta(param('udp_port'));         } 
else { $udp_port = $udp_port;  } } else { $udp_port = quotemeta($query{'udp_port'});   }
if ( !$query{'debug'} )   { if ( param('debug')  ) { $debug = quotemeta(param('debug'));         } 
else { $debug = $debug;  } } else { $debug = quotemeta($query{'debug'});   }


if ( !$query{'r1_active'} )   { if ( param('r1_active')  ) { $r1_active = quotemeta(param('r1_active'));         } 
else { $r1_active = $r1_active;  } } else { $r1_active = quotemeta($query{'r1_active'});   }
if ( !$query{'r1_send_status'} )   { if ( param('r1_send_status')  ) { $r1_send_status = quotemeta(param('r1_send_status'));         } 
else { $r1_send_status = $r1_send_status;  } } else { $r1_send_status = quotemeta($query{'r1_send_status'});   }
if ( !$query{'r1_send_consumables'} )   { if ( param('r1_send_consumables')  ) { $r1_send_consumables = quotemeta(param('r1_send_consumables'));         } 
else { $r1_send_consumables = $r1_send_consumables;  } } else { $r1_send_consumables = quotemeta($query{'r1_send_consumables'});   }
if ( !$query{'r1_send_cleaning_history'} )   { if ( param('r1_send_cleaning_history')  ) { $r1_send_cleaning_history = quotemeta(param('r1_send_cleaning_history'));         } 
else { $r1_send_cleaning_history = $r1_send_cleaning_history;  } } else { $r1_send_cleaning_history = quotemeta($query{'r1_send_cleaning_history'});   }
if ( !$query{'r1_mi_robo_ip'} )   { if ( param('r1_mi_robo_ip')  ) { $r1_mi_robo_ip = quotemeta(param('r1_mi_robo_ip'));         } 
else { $r1_mi_robo_ip = $r1_mi_robo_ip;  } } else { $r1_mi_robo_ip = quotemeta($query{'r1_mi_robo_ip'});   }
if ( !$query{'r1_mi_robo_token'} )   { if ( param('r1_mi_robo_token')  ) { $r1_mi_robo_token = quotemeta(param('r1_mi_robo_token'));         } 
else { $r1_mi_robo_token = $r1_mi_robo_token;  } } else { $r1_mi_robo_token = quotemeta($query{'r1_mi_robo_token'});   }
if ( !$query{'r1_vi_dnd'} )   { if ( param('r1_vi_dnd')  ) { $r1_vi_dnd = quotemeta(param('r1_vi_dnd'));         } 
else { $r1_vi_dnd = $r1_vi_dnd;  } } else { $r1_vi_dnd = quotemeta($query{'r1_vi_dnd'});   }
if ( !$query{'r1_vti_state'} )   { if ( param('r1_vti_state')  ) { $r1_vti_state = quotemeta(param('r1_vti_state'));         } 
else { $r1_vti_state = $r1_vti_state;  } } else { $r1_vti_state = quotemeta($query{'r1_vti_state'});   }
if ( !$query{'r1_vi_state_code'} )   { if ( param('r1_vi_state_code')  ) { $r1_vi_state_code = quotemeta(param('r1_vi_state_code'));         } 
else { $r1_vi_state_code = $r1_vi_state_code;  } } else { $r1_vi_state_code = quotemeta($query{'r1_vi_state_code'});   }
if ( !$query{'r1_vti_error'} )   { if ( param('r1_vti_error')  ) { $r1_vti_error = quotemeta(param('r1_vti_error'));         } 
else { $r1_vti_error = $r1_vti_error;  } } else { $r1_vti_error = quotemeta($query{'r1_vti_error'});   }
if ( !$query{'r1_vi_error_code'} )   { if ( param('r1_vi_error_code')  ) { $r1_vi_error_code = quotemeta(param('r1_vi_error_code'));         } 
else { $r1_vi_error_code = $r1_vi_error_code;  } } else { $r1_vi_error_code = quotemeta($query{'r1_vi_error_code'});   }
if ( !$query{'r1_vi_battery'} )   { if ( param('r1_vi_battery')  ) { $r1_vi_battery = quotemeta(param('r1_vi_battery'));         } 
else { $r1_vi_battery = $r1_vi_battery;  } } else { $r1_vi_battery = quotemeta($query{'r1_vi_battery'});   }
if ( !$query{'r1_vi_area'} )   { if ( param('r1_vi_area')  ) { $r1_vi_area = quotemeta(param('r1_vi_area'));         } 
else { $r1_vi_area = $r1_vi_area;  } } else { $r1_vi_area = quotemeta($query{'r1_vi_area'});   }
if ( !$query{'r1_vi_time'} )   { if ( param('r1_vi_time')  ) { $r1_vi_time = quotemeta(param('r1_vi_time'));         } 
else { $r1_vi_time = $r1_vi_time;  } } else { $r1_vi_time = quotemeta($query{'r1_vi_time'});   }
if ( !$query{'r1_vi_fanspeed'} )   { if ( param('r1_vi_fanspeed')  ) { $r1_vi_fanspeed = quotemeta(param('r1_vi_fanspeed'));         } 
else { $r1_vi_fanspeed = $r1_vi_fanspeed;  } } else { $r1_vi_fanspeed = quotemeta($query{'r1_vi_fanspeed'});   }
if ( !$query{'r1_vi_mainbrush'} )   { if ( param('r1_vi_mainbrush')  ) { $r1_vi_mainbrush = quotemeta(param('r1_vi_mainbrush'));         } 
else { $r1_vi_mainbrush = $r1_vi_mainbrush;  } } else { $r1_vi_mainbrush = quotemeta($query{'r1_vi_mainbrush'});   }
if ( !$query{'r1_vi_sidebrush'} )   { if ( param('r1_vi_sidebrush')  ) { $r1_vi_sidebrush = quotemeta(param('r1_vi_sidebrush'));         } 
else { $r1_vi_sidebrush = $r1_vi_sidebrush;  } } else { $r1_vi_sidebrush = quotemeta($query{'r1_vi_sidebrush'});   }
if ( !$query{'r1_vi_filter'} )   { if ( param('r1_vi_filter')  ) { $r1_vi_filter = quotemeta(param('r1_vi_filter'));         } 
else { $r1_vi_filter = $r1_vi_filter;  } } else { $r1_vi_filter = quotemeta($query{'r1_vi_filter'});   }
if ( !$query{'r1_vi_sensor'} )   { if ( param('r1_vi_sensor')  ) { $r1_vi_sensor = quotemeta(param('r1_vi_sensor'));         } 
else { $r1_vi_sensor = $r1_vi_sensor;  } } else { $r1_vi_sensor = quotemeta($query{'r1_vi_sensor'});   }
if ( !$query{'r1_vi_ch_count'} )   { if ( param('r1_vi_ch_count')  ) { $r1_vi_ch_count = quotemeta(param('r1_vi_ch_count'));         } 
else { $r1_vi_ch_count = $r1_vi_ch_count;  } } else { $r1_vi_ch_count = quotemeta($query{'r1_vi_ch_count'});   }
if ( !$query{'r1_vi_ch_area'} )   { if ( param('r1_vi_ch_area')  ) { $r1_vi_ch_area = quotemeta(param('r1_vi_ch_area'));         } 
else { $r1_vi_ch_area = $r1_vi_ch_area;  } } else { $r1_vi_ch_area = quotemeta($query{'r1_vi_ch_area'});   }
if ( !$query{'r1_vi_ch_time'} )   { if ( param('r1_vi_ch_time')  ) { $r1_vi_ch_time = quotemeta(param('r1_vi_ch_time'));         } 
else { $r1_vi_ch_time = $r1_vi_ch_time;  } } else { $r1_vi_ch_time = quotemeta($query{'r1_vi_ch_time'});   }

if ( !$query{'r2_active'} )   { if ( param('r2_active')  ) { $r2_active = quotemeta(param('r2_active'));         } 
else { $r2_active = $r2_active;  } } else { $r2_active = quotemeta($query{'r2_active'});   }
if ( !$query{'r2_send_status'} )   { if ( param('r2_send_status')  ) { $r2_send_status = quotemeta(param('r2_send_status'));         } 
else { $r2_send_status = $r2_send_status;  } } else { $r2_send_status = quotemeta($query{'r2_send_status'});   }
if ( !$query{'r2_send_consumables'} )   { if ( param('r2_send_consumables')  ) { $r2_send_consumables = quotemeta(param('r2_send_consumables'));         } 
else { $r2_send_consumables = $r2_send_consumables;  } } else { $r2_send_consumables = quotemeta($query{'r2_send_consumables'});   }
if ( !$query{'r2_send_cleaning_history'} )   { if ( param('r2_send_cleaning_history')  ) { $r2_send_cleaning_history = quotemeta(param('r2_send_cleaning_history'));         } 
else { $r2_send_cleaning_history = $r2_send_cleaning_history;  } } else { $r2_send_cleaning_history = quotemeta($query{'r2_send_cleaning_history'});   }
if ( !$query{'r2_mi_robo_ip'} )   { if ( param('r2_mi_robo_ip')  ) { $r2_mi_robo_ip = quotemeta(param('r2_mi_robo_ip'));         } 
else { $r2_mi_robo_ip = $r2_mi_robo_ip;  } } else { $r2_mi_robo_ip = quotemeta($query{'r2_mi_robo_ip'});   }
if ( !$query{'r2_mi_robo_token'} )   { if ( param('r2_mi_robo_token')  ) { $r2_mi_robo_token = quotemeta(param('r2_mi_robo_token'));         } 
else { $r2_mi_robo_token = $r2_mi_robo_token;  } } else { $r2_mi_robo_token = quotemeta($query{'r2_mi_robo_token'});   }
if ( !$query{'r2_vi_dnd'} )   { if ( param('r2_vi_dnd')  ) { $r2_vi_dnd = quotemeta(param('r2_vi_dnd'));         } 
else { $r2_vi_dnd = $r2_vi_dnd;  } } else { $r2_vi_dnd = quotemeta($query{'r2_vi_dnd'});   }
if ( !$query{'r2_vti_state'} )   { if ( param('r2_vti_state')  ) { $r2_vti_state = quotemeta(param('r2_vti_state'));         } 
else { $r2_vti_state = $r2_vti_state;  } } else { $r2_vti_state = quotemeta($query{'r2_vti_state'});   }
if ( !$query{'r2_vi_state_code'} )   { if ( param('r2_vi_state_code')  ) { $r2_vi_state_code = quotemeta(param('r2_vi_state_code'));         } 
else { $r2_vi_state_code = $r2_vi_state_code;  } } else { $r2_vi_state_code = quotemeta($query{'r2_vi_state_code'});   }
if ( !$query{'r2_vti_error'} )   { if ( param('r2_vti_error')  ) { $r2_vti_error = quotemeta(param('r2_vti_error'));         } 
else { $r2_vti_error = $r2_vti_error;  } } else { $r2_vti_error = quotemeta($query{'r2_vti_error'});   }
if ( !$query{'r2_vi_error_code'} )   { if ( param('r2_vi_error_code')  ) { $r2_vi_error_code = quotemeta(param('r2_vi_error_code'));         } 
else { $r2_vi_error_code = $r2_vi_error_code;  } } else { $r2_vi_error_code = quotemeta($query{'r2_vi_error_code'});   }
if ( !$query{'r2_vi_battery'} )   { if ( param('r2_vi_battery')  ) { $r2_vi_battery = quotemeta(param('r2_vi_battery'));         } 
else { $r2_vi_battery = $r2_vi_battery;  } } else { $r2_vi_battery = quotemeta($query{'r2_vi_battery'});   }
if ( !$query{'r2_vi_area'} )   { if ( param('r2_vi_area')  ) { $r2_vi_area = quotemeta(param('r2_vi_area'));         } 
else { $r2_vi_area = $r2_vi_area;  } } else { $r2_vi_area = quotemeta($query{'r2_vi_area'});   }
if ( !$query{'r2_vi_time'} )   { if ( param('r2_vi_time')  ) { $r2_vi_time = quotemeta(param('r2_vi_time'));         } 
else { $r2_vi_time = $r2_vi_time;  } } else { $r2_vi_time = quotemeta($query{'r2_vi_time'});   }
if ( !$query{'r2_vi_fanspeed'} )   { if ( param('r2_vi_fanspeed')  ) { $r2_vi_fanspeed = quotemeta(param('r2_vi_fanspeed'));         } 
else { $r2_vi_fanspeed = $r2_vi_fanspeed;  } } else { $r2_vi_fanspeed = quotemeta($query{'r2_vi_fanspeed'});   }
if ( !$query{'r2_vi_mainbrush'} )   { if ( param('r2_vi_mainbrush')  ) { $r2_vi_mainbrush = quotemeta(param('r2_vi_mainbrush'));         } 
else { $r2_vi_mainbrush = $r2_vi_mainbrush;  } } else { $r2_vi_mainbrush = quotemeta($query{'r2_vi_mainbrush'});   }
if ( !$query{'r2_vi_sidebrush'} )   { if ( param('r2_vi_sidebrush')  ) { $r2_vi_sidebrush = quotemeta(param('r2_vi_sidebrush'));         } 
else { $r2_vi_sidebrush = $r2_vi_sidebrush;  } } else { $r2_vi_sidebrush = quotemeta($query{'r2_vi_sidebrush'});   }
if ( !$query{'r2_vi_filter'} )   { if ( param('r2_vi_filter')  ) { $r2_vi_filter = quotemeta(param('r2_vi_filter'));         } 
else { $r2_vi_filter = $r2_vi_filter;  } } else { $r2_vi_filter = quotemeta($query{'r2_vi_filter'});   }
if ( !$query{'r2_vi_sensor'} )   { if ( param('r2_vi_sensor')  ) { $r2_vi_sensor = quotemeta(param('r2_vi_sensor'));         } 
else { $r2_vi_sensor = $r2_vi_sensor;  } } else { $r2_vi_sensor = quotemeta($query{'r2_vi_sensor'});   }
if ( !$query{'r2_vi_ch_count'} )   { if ( param('r2_vi_ch_count')  ) { $r2_vi_ch_count = quotemeta(param('r2_vi_ch_count'));         } 
else { $r2_vi_ch_count = $r2_vi_ch_count;  } } else { $r2_vi_ch_count = quotemeta($query{'r2_vi_ch_count'});   }
if ( !$query{'r2_vi_ch_area'} )   { if ( param('r2_vi_ch_area')  ) { $r2_vi_ch_area = quotemeta(param('r2_vi_ch_area'));         } 
else { $r2_vi_ch_area = $r2_vi_ch_area;  } } else { $r2_vi_ch_area = quotemeta($query{'r2_vi_ch_area'});   }
if ( !$query{'r2_vi_ch_time'} )   { if ( param('r2_vi_ch_time')  ) { $r2_vi_ch_time = quotemeta(param('r2_vi_ch_time'));         } 
else { $r2_vi_ch_time = $r2_vi_ch_time;  } } else { $r2_vi_ch_time = quotemeta($query{'r2_vi_ch_time'});   }

if ( !$query{'r3_active'} )   { if ( param('r3_active')  ) { $r3_active = quotemeta(param('r3_active'));         } 
else { $r3_active = $r3_active;  } } else { $r3_active = quotemeta($query{'r3_active'});   }
if ( !$query{'r3_send_status'} )   { if ( param('r3_send_status')  ) { $r3_send_status = quotemeta(param('r3_send_status'));         } 
else { $r3_send_status = $r3_send_status;  } } else { $r3_send_status = quotemeta($query{'r3_send_status'});   }
if ( !$query{'r3_send_consumables'} )   { if ( param('r3_send_consumables')  ) { $r3_send_consumables = quotemeta(param('r3_send_consumables'));         } 
else { $r3_send_consumables = $r3_send_consumables;  } } else { $r3_send_consumables = quotemeta($query{'r3_send_consumables'});   }
if ( !$query{'r3_send_cleaning_history'} )   { if ( param('r3_send_cleaning_history')  ) { $r3_send_cleaning_history = quotemeta(param('r3_send_cleaning_history'));         } 
else { $r3_send_cleaning_history = $r3_send_cleaning_history;  } } else { $r3_send_cleaning_history = quotemeta($query{'r3_send_cleaning_history'});   }
if ( !$query{'r3_mi_robo_ip'} )   { if ( param('r3_mi_robo_ip')  ) { $r3_mi_robo_ip = quotemeta(param('r3_mi_robo_ip'));         } 
else { $r3_mi_robo_ip = $r3_mi_robo_ip;  } } else { $r3_mi_robo_ip = quotemeta($query{'r3_mi_robo_ip'});   }
if ( !$query{'r3_mi_robo_token'} )   { if ( param('r3_mi_robo_token')  ) { $r3_mi_robo_token = quotemeta(param('r3_mi_robo_token'));         } 
else { $r3_mi_robo_token = $r3_mi_robo_token;  } } else { $r3_mi_robo_token = quotemeta($query{'r3_mi_robo_token'});   }
if ( !$query{'r3_vi_dnd'} )   { if ( param('r3_vi_dnd')  ) { $r3_vi_dnd = quotemeta(param('r3_vi_dnd'));         } 
else { $r3_vi_dnd = $r3_vi_dnd;  } } else { $r3_vi_dnd = quotemeta($query{'r3_vi_dnd'});   }
if ( !$query{'r3_vti_state'} )   { if ( param('r3_vti_state')  ) { $r3_vti_state = quotemeta(param('r3_vti_state'));         } 
else { $r3_vti_state = $r3_vti_state;  } } else { $r3_vti_state = quotemeta($query{'r3_vti_state'});   }
if ( !$query{'r3_vi_state_code'} )   { if ( param('r3_vi_state_code')  ) { $r3_vi_state_code = quotemeta(param('r3_vi_state_code'));         } 
else { $r3_vi_state_code = $r3_vi_state_code;  } } else { $r3_vi_state_code = quotemeta($query{'r3_vi_state_code'});   }
if ( !$query{'r3_vti_error'} )   { if ( param('r3_vti_error')  ) { $r3_vti_error = quotemeta(param('r3_vti_error'));         } 
else { $r3_vti_error = $r3_vti_error;  } } else { $r3_vti_error = quotemeta($query{'r3_vti_error'});   }
if ( !$query{'r3_vi_error_code'} )   { if ( param('r3_vi_error_code')  ) { $r3_vi_error_code = quotemeta(param('r3_vi_error_code'));         } 
else { $r3_vi_error_code = $r3_vi_error_code;  } } else { $r3_vi_error_code = quotemeta($query{'r3_vi_error_code'});   }
if ( !$query{'r3_vi_battery'} )   { if ( param('r3_vi_battery')  ) { $r3_vi_battery = quotemeta(param('r3_vi_battery'));         } 
else { $r3_vi_battery = $r3_vi_battery;  } } else { $r3_vi_battery = quotemeta($query{'r3_vi_battery'});   }
if ( !$query{'r3_vi_area'} )   { if ( param('r3_vi_area')  ) { $r3_vi_area = quotemeta(param('r3_vi_area'));         } 
else { $r3_vi_area = $r3_vi_area;  } } else { $r3_vi_area = quotemeta($query{'r3_vi_area'});   }
if ( !$query{'r3_vi_time'} )   { if ( param('r3_vi_time')  ) { $r3_vi_time = quotemeta(param('r3_vi_time'));         } 
else { $r3_vi_time = $r3_vi_time;  } } else { $r3_vi_time = quotemeta($query{'r3_vi_time'});   }
if ( !$query{'r3_vi_fanspeed'} )   { if ( param('r3_vi_fanspeed')  ) { $r3_vi_fanspeed = quotemeta(param('r3_vi_fanspeed'));         } 
else { $r3_vi_fanspeed = $r3_vi_fanspeed;  } } else { $r3_vi_fanspeed = quotemeta($query{'r3_vi_fanspeed'});   }
if ( !$query{'r3_vi_mainbrush'} )   { if ( param('r3_vi_mainbrush')  ) { $r3_vi_mainbrush = quotemeta(param('r3_vi_mainbrush'));         } 
else { $r3_vi_mainbrush = $r3_vi_mainbrush;  } } else { $r3_vi_mainbrush = quotemeta($query{'r3_vi_mainbrush'});   }
if ( !$query{'r3_vi_sidebrush'} )   { if ( param('r3_vi_sidebrush')  ) { $r3_vi_sidebrush = quotemeta(param('r3_vi_sidebrush'));         } 
else { $r3_vi_sidebrush = $r3_vi_sidebrush;  } } else { $r3_vi_sidebrush = quotemeta($query{'r3_vi_sidebrush'});   }
if ( !$query{'r3_vi_filter'} )   { if ( param('r3_vi_filter')  ) { $r3_vi_filter = quotemeta(param('r3_vi_filter'));         } 
else { $r3_vi_filter = $r3_vi_filter;  } } else { $r3_vi_filter = quotemeta($query{'r3_vi_filter'});   }
if ( !$query{'r3_vi_sensor'} )   { if ( param('r3_vi_sensor')  ) { $r3_vi_sensor = quotemeta(param('r3_vi_sensor'));         } 
else { $r3_vi_sensor = $r3_vi_sensor;  } } else { $r3_vi_sensor = quotemeta($query{'r3_vi_sensor'});   }
if ( !$query{'r3_vi_ch_count'} )   { if ( param('r3_vi_ch_count')  ) { $r3_vi_ch_count = quotemeta(param('r3_vi_ch_count'));         } 
else { $r3_vi_ch_count = $r3_vi_ch_count;  } } else { $r3_vi_ch_count = quotemeta($query{'r3_vi_ch_count'});   }
if ( !$query{'r3_vi_ch_area'} )   { if ( param('r3_vi_ch_area')  ) { $r3_vi_ch_area = quotemeta(param('r3_vi_ch_area'));         } 
else { $r3_vi_ch_area = $r3_vi_ch_area;  } } else { $r3_vi_ch_area = quotemeta($query{'r3_vi_ch_area'});   }
if ( !$query{'r3_vi_ch_time'} )   { if ( param('r3_vi_ch_time')  ) { $r3_vi_ch_time = quotemeta(param('r3_vi_ch_time'));         } 
else { $r3_vi_ch_time = $r3_vi_ch_time;  } } else { $r3_vi_ch_time = quotemeta($query{'r3_vi_ch_time'});   }

# Figure out in which subfolder we are installed
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

# Save settings to config file
if (param('savedata')) {
	$conf = new Config::Simple("$home/config/plugins/$psubfolder/mi.cfg");
	if ($debug ne 1) { $debug = 0 }
	if ($r1_active ne 1) { $r1_active = 0 }
	if ($r1_send_status ne 1) { $r1_send_status = 0 }
	if ($r1_send_consumables ne 1) { $r1_send_consumables = 0 }
	if ($r1_send_cleaning_history ne 1) { $r1_send_cleaning_history = 0 }
	if ($r2_active ne 1) { $r2_active = 0 }
	if ($r2_send_status ne 1) { $r2_send_status = 0 }
	if ($r2_send_consumables ne 1) { $r2_send_consumables = 0 }
	if ($r2_send_cleaning_history ne 1) { $r2_send_cleaning_history = 0 }
	if ($r3_active ne 1) { $r3_active = 0 }
	if ($r3_send_status ne 1) { $r3_send_status = 0 }
	if ($r3_send_consumables ne 1) { $r3_send_consumables = 0 }
	if ($r3_send_cleaning_history ne 1) { $r3_send_cleaning_history = 0 }
	$conf->param('LANGUAGE', unquotemeta($language));	
	$conf->param('LOOPTIME', unquotemeta($looptime));	
	$conf->param('UDP_PORT', unquotemeta($udp_port));
	$conf->param('DEBUG', unquotemeta($debug));		

	$conf->param('R1_MI_ROBO_IP', unquotemeta($r1_mi_robo_ip));
	$conf->param('R1_MI_ROBO_TOKEN', unquotemeta($r1_mi_robo_token));		
	$conf->param('R1_ACTIVE', unquotemeta($r1_active));
	$conf->param('R1_SEND_CONSUMABLES', unquotemeta($r1_send_consumables));
	$conf->param('R1_VI_MAINBRUSH', unquotemeta($r1_vi_mainbrush));	
	$conf->param('R1_VI_SIDEBRUSH', unquotemeta($r1_vi_sidebrush));		
	$conf->param('R1_VI_FILTER', unquotemeta($r1_vi_filter));
	$conf->param('R1_VI_SENSOR', unquotemeta($r1_vi_sensor));		
	$conf->param('R1_SEND_STATUS', unquotemeta($r1_send_status));	
	$conf->param('R1_VTI_ERROR', unquotemeta($r1_vti_error));
	$conf->param('R1_VI_ERROR_CODE', unquotemeta($r1_vi_error_code));	
	$conf->param('R1_VTI_STATE', unquotemeta($r1_vti_state));
	$conf->param('R1_VI_STATE_CODE', unquotemeta($r1_vi_state_code));	
	$conf->param('R1_VI_BATTERY', unquotemeta($r1_vi_battery));
	$conf->param('R1_VI_FANSPEED', unquotemeta($r1_vi_fanspeed));
	$conf->param('R1_VI_AREA', unquotemeta($r1_vi_area));
	$conf->param('R1_VI_TIME', unquotemeta($r1_vi_time));		
	$conf->param('R1_VI_DND', unquotemeta($r1_vi_dnd));		
	$conf->param('R1_SEND_CLEANING_HISTORY', unquotemeta($r1_send_cleaning_history));
	$conf->param('R1_VI_CH_TIME', unquotemeta($r1_vi_ch_time));
	$conf->param('R1_VI_CH_COUNT', unquotemeta($r1_vi_ch_count));
	$conf->param('R1_VI_CH_AREA', unquotemeta($r1_vi_ch_area));	

	$conf->param('R2_MI_ROBO_IP', unquotemeta($r2_mi_robo_ip));
	$conf->param('R2_MI_ROBO_TOKEN', unquotemeta($r2_mi_robo_token));		
	$conf->param('R2_ACTIVE', unquotemeta($r2_active));	
	$conf->param('R2_SEND_CONSUMABLES', unquotemeta($r2_send_consumables));
	$conf->param('R2_VI_MAINBRUSH', unquotemeta($r2_vi_mainbrush));	
	$conf->param('R2_VI_SIDEBRUSH', unquotemeta($r2_vi_sidebrush));		
	$conf->param('R2_VI_FILTER', unquotemeta($r2_vi_filter));
	$conf->param('R2_VI_SENSOR', unquotemeta($r2_vi_sensor));		
	$conf->param('R2_SEND_STATUS', unquotemeta($r2_send_status));	
	$conf->param('R2_VTI_ERROR', unquotemeta($r2_vti_error));
	$conf->param('R2_VI_ERROR_CODE', unquotemeta($r2_vi_error_code));	
	$conf->param('R2_VTI_STATE', unquotemeta($r2_vti_state));
	$conf->param('R2_VI_STATE_CODE', unquotemeta($r2_vi_state_code));	
	$conf->param('R2_VI_BATTERY', unquotemeta($r2_vi_battery));
	$conf->param('R2_VI_FANSPEED', unquotemeta($r2_vi_fanspeed));
	$conf->param('R2_VI_AREA', unquotemeta($r2_vi_area));
	$conf->param('R2_VI_TIME', unquotemeta($r2_vi_time));		
	$conf->param('R2_VI_DND', unquotemeta($r2_vi_dnd));		
	$conf->param('R2_SEND_CLEANING_HISTORY', unquotemeta($r2_send_cleaning_history));
	$conf->param('R2_VI_CH_TIME', unquotemeta($r2_vi_ch_time));
	$conf->param('R2_VI_CH_COUNT', unquotemeta($r2_vi_ch_count));
	$conf->param('R2_VI_CH_AREA', unquotemeta($r2_vi_ch_area));	
	
	
	$conf->param('R3_MI_ROBO_IP', unquotemeta($r3_mi_robo_ip));
	$conf->param('R3_MI_ROBO_TOKEN', unquotemeta($r3_mi_robo_token));		
	$conf->param('R3_ACTIVE', unquotemeta($r3_active));	
	$conf->param('R3_SEND_CONSUMABLES', unquotemeta($r3_send_consumables));
	$conf->param('R3_VI_MAINBRUSH', unquotemeta($r3_vi_mainbrush));	
	$conf->param('R3_VI_SIDEBRUSH', unquotemeta($r3_vi_sidebrush));		
	$conf->param('R3_VI_FILTER', unquotemeta($r3_vi_filter));
	$conf->param('R3_VI_SENSOR', unquotemeta($r3_vi_sensor));		
	$conf->param('R3_SEND_STATUS', unquotemeta($r3_send_status));	
	$conf->param('R3_VTI_ERROR', unquotemeta($r3_vti_error));
	$conf->param('R3_VI_ERROR_CODE', unquotemeta($r3_vi_error_code));	
	$conf->param('R3_VTI_STATE', unquotemeta($r3_vti_state));
	$conf->param('R3_VI_STATE_CODE', unquotemeta($r3_vi_state_code));	
	$conf->param('R3_VI_BATTERY', unquotemeta($r3_vi_battery));
	$conf->param('R3_VI_FANSPEED', unquotemeta($r3_vi_fanspeed));
	$conf->param('R3_VI_AREA', unquotemeta($r3_vi_area));
	$conf->param('R3_VI_TIME', unquotemeta($r3_vi_time));		
	$conf->param('R3_VI_DND', unquotemeta($r3_vi_dnd));		
	$conf->param('R3_SEND_CLEANING_HISTORY', unquotemeta($r3_send_cleaning_history));
	$conf->param('R3_VI_CH_TIME', unquotemeta($r3_vi_ch_time));
	$conf->param('R3_VI_CH_COUNT', unquotemeta($r3_vi_ch_count));
	$conf->param('R3_VI_CH_AREA', unquotemeta($r3_vi_ch_area));

	$conf->param('MINISERVER_IP', unquotemeta($miniserver_ip));
	$conf->param('MINISERVER_USER', unquotemeta($miniserver_user));
	$conf->param('MINISERVER_PASS', unquotemeta($miniserver_pass));
	
	$conf->save();
}

# Parse config file
$conf = new Config::Simple("$home/config/plugins/$psubfolder/mi.cfg");
$language = encode_entities($conf->param('LANGUAGE'));	
$looptime = encode_entities($conf->param('LOOPTIME'));	
$udp_port = encode_entities($conf->param('UDP_PORT'));
$debug = encode_entities($conf->param('DEBUG'));

$r1_mi_robo_ip = encode_entities($conf->param('R1_MI_ROBO_IP'));
$r1_mi_robo_token = encode_entities($conf->param('R1_MI_ROBO_TOKEN'));	
$r1_active = encode_entities($conf->param('R1_ACTIVE'));
$r1_send_status = encode_entities($conf->param('R1_SEND_STATUS'));	
$r1_vti_state = encode_entities($conf->param('R1_VTI_STATE'));
$r1_vi_state_code = encode_entities($conf->param('R1_VI_STATE_CODE'));
$r1_vti_error = encode_entities($conf->param('R1_VTI_ERROR'));
$r1_vi_error_code = encode_entities($conf->param('R1_VI_ERROR_CODE'));
$r1_vi_battery = encode_entities($conf->param('R1_VI_BATTERY'));
$r1_vi_fanspeed = encode_entities($conf->param('R1_VI_FANSPEED'));
$r1_vi_area = encode_entities($conf->param('R1_VI_AREA'));
$r1_vi_time = encode_entities($conf->param('R1_VI_TIME'));
$r1_vi_dnd = encode_entities($conf->param('R1_VI_DND'));
$r1_send_consumables = encode_entities($conf->param('R1_SEND_CONSUMABLES'));
$r1_vi_sidebrush = encode_entities($conf->param('R1_VI_SIDEBRUSH'));	
$r1_vi_mainbrush = encode_entities($conf->param('R1_VI_MAINBRUSH'));	
$r1_vi_filter = encode_entities($conf->param('R1_VI_FILTER'));
$r1_vi_sensor = encode_entities($conf->param('R1_VI_SENSOR'));
$r1_send_cleaning_history = encode_entities($conf->param('R1_SEND_CLEANING_HISTORY'));		
$r1_vi_ch_time = encode_entities($conf->param('R1_VI_CH_TIME'));
$r1_vi_ch_count = encode_entities($conf->param('R1_VI_CH_COUNT'));
$r1_vi_ch_area = encode_entities($conf->param('R1_VI_CH_AREA'));

$r2_mi_robo_ip = encode_entities($conf->param('R2_MI_ROBO_IP'));
$r2_mi_robo_token = encode_entities($conf->param('R2_MI_ROBO_TOKEN'));	
$r2_active = encode_entities($conf->param('R2_ACTIVE'));
$r2_send_status = encode_entities($conf->param('R2_SEND_STATUS'));	
$r2_vti_state = encode_entities($conf->param('R2_VTI_STATE'));
$r2_vi_state_code = encode_entities($conf->param('R2_VI_STATE_CODE'));
$r2_vti_error = encode_entities($conf->param('R2_VTI_ERROR'));
$r2_vi_error_code = encode_entities($conf->param('R2_VI_ERROR_CODE'));
$r2_vi_battery = encode_entities($conf->param('R2_VI_BATTERY'));
$r2_vi_fanspeed = encode_entities($conf->param('R2_VI_FANSPEED'));
$r2_vi_area = encode_entities($conf->param('R2_VI_AREA'));
$r2_vi_time = encode_entities($conf->param('R2_VI_TIME'));
$r2_vi_dnd = encode_entities($conf->param('R2_VI_DND'));
$r2_send_consumables = encode_entities($conf->param('R2_SEND_CONSUMABLES'));
$r2_vi_sidebrush = encode_entities($conf->param('R2_VI_SIDEBRUSH'));	
$r2_vi_mainbrush = encode_entities($conf->param('R2_VI_MAINBRUSH'));	
$r2_vi_filter = encode_entities($conf->param('R2_VI_FILTER'));
$r2_vi_sensor = encode_entities($conf->param('R2_VI_SENSOR'));
$r2_send_cleaning_history = encode_entities($conf->param('R2_SEND_CLEANING_HISTORY'));		
$r2_vi_ch_time = encode_entities($conf->param('R2_VI_CH_TIME'));
$r2_vi_ch_count = encode_entities($conf->param('R2_VI_CH_COUNT'));
$r2_vi_ch_area = encode_entities($conf->param('R2_VI_CH_AREA'));

$r3_mi_robo_ip = encode_entities($conf->param('R3_MI_ROBO_IP'));
$r3_mi_robo_token = encode_entities($conf->param('R3_MI_ROBO_TOKEN'));	
$r3_active = encode_entities($conf->param('R3_ACTIVE'));
$r3_send_status = encode_entities($conf->param('R3_SEND_STATUS'));	
$r3_vti_state = encode_entities($conf->param('R3_VTI_STATE'));
$r3_vi_state_code = encode_entities($conf->param('R3_VI_STATE_CODE'));
$r3_vti_error = encode_entities($conf->param('R3_VTI_ERROR'));
$r3_vi_error_code = encode_entities($conf->param('R3_VI_ERROR_CODE'));
$r3_vi_battery = encode_entities($conf->param('R3_VI_BATTERY'));
$r3_vi_fanspeed = encode_entities($conf->param('R3_VI_FANSPEED'));
$r3_vi_area = encode_entities($conf->param('R3_VI_AREA'));
$r3_vi_time = encode_entities($conf->param('R3_VI_TIME'));
$r3_vi_dnd = encode_entities($conf->param('R3_VI_DND'));
$r3_send_consumables = encode_entities($conf->param('R3_SEND_CONSUMABLES'));
$r3_vi_sidebrush = encode_entities($conf->param('R3_VI_SIDEBRUSH'));	
$r3_vi_mainbrush = encode_entities($conf->param('R3_VI_MAINBRUSH'));	
$r3_vi_filter = encode_entities($conf->param('R3_VI_FILTER'));
$r3_vi_sensor = encode_entities($conf->param('R3_VI_SENSOR'));
$r3_send_cleaning_history = encode_entities($conf->param('R3_SEND_CLEANING_HISTORY'));		
$r3_vi_ch_time = encode_entities($conf->param('R3_VI_CH_TIME'));
$r3_vi_ch_count = encode_entities($conf->param('R3_VI_CH_COUNT'));
$r3_vi_ch_area = encode_entities($conf->param('R3_VI_CH_AREA'));


# Set Enabled / Disabled switch
if ($r1_active eq "1") {
	$r1_select_active = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r1_select_active = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r1_send_status eq "1") {
	$r1_select_status = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r1_select_status = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r1_send_consumables eq "1") {
	$r1_select_consumables = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r1_select_consumables = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r1_send_cleaning_history eq "1") {
	$r1_select_chistory = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r1_select_chistory = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r2_active eq "1") {
	$r2_select_active = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r2_select_active = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r2_send_status eq "1") {
	$r2_select_status = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r2_select_status = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r2_send_consumables eq "1") {
	$r2_select_consumables = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r2_select_consumables = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r2_send_cleaning_history eq "1") {
	$r2_select_chistory = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r2_select_chistory = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r3_active eq "1") {
	$r3_select_active = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r3_select_active = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r3_send_status eq "1") {
	$r3_select_status = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r3_select_status = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r3_send_consumables eq "1") {
	$r3_select_consumables = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r3_select_consumables = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($r3_send_cleaning_history eq "1") {
	$r3_select_chistory = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$r3_select_chistory = '<option value="0" selected>off</option><option value="1">on</option>';
}


if ($debug eq "1") {
	$select_debug = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$select_debug = '<option value="0" selected>off</option><option value="1">on</option>';
}
# Set Language
if ($language eq "de") {
	$select_language = '<option selected value="de">german</option><option value="en">english</option>\n';
} else {
	$select_language = '<option selected value="en">english</option><option value="de">german</option>\n';
}

# Title
$template_title = "MIRobo2Lox";

# Create help page
$helptext = "<b>Hilfe</b><br>Wenn ihr Hilfe beim Einrichten benötigt findet ihr diese im LoxWiki.";
$helptext = $helptext . "<br><a href='http://www.loxwiki.eu/display/LOXBERRY/MiRobot2Lox' target='_blank'>LoxWiki - MiRobot2Lox</a>";
$helptext = $helptext . "<br><br><b>Debug/Log</b><br>Um Debug zu starten, den Schalter auf on stellen und speichern.<br>Die Log-Datei kann hier eingesehen werden. ";
$helptext = $helptext . "<a href='http://loxberry/admin/system/tools/logfile.cgi?logfile=plugins/mirobot2lox/mirobot2lox.log&header=txt' target='_blank'>Log-File - MiRobot2Lox</a>";
$helptext = $helptext . "<br><br><b>Achtung!</b> Wenn Debug aktiv ist werden sehr viele Daten ins Log geschrieben. Bitte nur bei Problemen nutzen.";


# Currently only german is supported - so overwrite user language settings:
$lang = "de";

# Load header and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
open(F,"$installfolder/templates/system/$lang/header.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# Load content from template
open(F,"$installfolder/templates/plugins/$psubfolder/$lang/content.html") || die "Missing template $lang/content.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# Load footer and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
open(F,"$installfolder/templates/system/$lang/footer.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

exit;
