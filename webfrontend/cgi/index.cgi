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
our $looptime;	
our $udp_port;	
our $send_consumables;
our $send_status;	
our $send_cleaning_history;		
our $mi_robo_ip;
our $mi_robo_token;		
our $vi_dnd;	
our $vi_sidebrush;	
our $vi_mainbrush;	
our $vi_filter;
our $vi_sensor;	
our $vti_state;
our $vi_state_code;
our $vti_error;
our $vi_error_code;
our $vi_battery;
our $vi_fanspeed;
our $vi_area;
our $vi_time;
our $vi_ch_time;
our $vi_ch_count;
our $vi_ch_area;
our $miniserver_ip;
our $miniserver_user;
our $miniserver_pass;
our $LANGselectlist;
our $Enabledstatus;
our $Enabledconsumables;
our $Enabledchistory;
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
if ( !$query{'send_status'} )   { if ( param('send_status')  ) { $send_status = quotemeta(param('send_status'));         } 
else { $send_status = $send_status;  } } else { $send_status = quotemeta($query{'send_status'});   }
if ( !$query{'send_consumables'} )   { if ( param('send_consumables')  ) { $send_consumables = quotemeta(param('send_consumables'));         } 
else { $send_consumables = $send_consumables;  } } else { $send_consumables = quotemeta($query{'send_consumables'});   }
if ( !$query{'send_cleaning_history'} )   { if ( param('send_cleaning_history')  ) { $send_cleaning_history = quotemeta(param('send_cleaning_history'));         } 
else { $send_cleaning_history = $send_cleaning_history;  } } else { $send_cleaning_history = quotemeta($query{'send_cleaning_history'});   }
if ( !$query{'mi_robo_ip'} )   { if ( param('mi_robo_ip')  ) { $mi_robo_ip = quotemeta(param('mi_robo_ip'));         } 
else { $mi_robo_ip = $mi_robo_ip;  } } else { $mi_robo_ip = quotemeta($query{'mi_robo_ip'});   }
if ( !$query{'mi_robo_token'} )   { if ( param('mi_robo_token')  ) { $mi_robo_token = quotemeta(param('mi_robo_token'));         } 
else { $mi_robo_token = $mi_robo_token;  } } else { $mi_robo_token = quotemeta($query{'mi_robo_token'});   }
if ( !$query{'vi_dnd'} )   { if ( param('vi_dnd')  ) { $vi_dnd = quotemeta(param('vi_dnd'));         } 
else { $vi_dnd = $vi_dnd;  } } else { $vi_dnd = quotemeta($query{'vi_dnd'});   }
if ( !$query{'vti_state'} )   { if ( param('vti_state')  ) { $vti_state = quotemeta(param('vti_state'));         } 
else { $vti_state = $vti_state;  } } else { $vti_state = quotemeta($query{'vti_state'});   }
if ( !$query{'vi_state_code'} )   { if ( param('vi_state_code')  ) { $vi_state_code = quotemeta(param('vi_state_code'));         } 
else { $vi_state_code = $vi_state_code;  } } else { $vi_state_code = quotemeta($query{'vi_state_code'});   }
if ( !$query{'vti_error'} )   { if ( param('vti_error')  ) { $vti_error = quotemeta(param('vti_error'));         } 
else { $vti_error = $vti_error;  } } else { $vti_error = quotemeta($query{'vti_error'});   }
if ( !$query{'vi_error_code'} )   { if ( param('vi_error_code')  ) { $vi_error_code = quotemeta(param('vi_error_code'));         } 
else { $vi_error_code = $vi_error_code;  } } else { $vi_error_code = quotemeta($query{'vi_error_code'});   }
if ( !$query{'vi_battery'} )   { if ( param('vi_battery')  ) { $vi_battery = quotemeta(param('vi_battery'));         } 
else { $vi_battery = $vi_battery;  } } else { $vi_battery = quotemeta($query{'vi_battery'});   }
if ( !$query{'vi_area'} )   { if ( param('vi_area')  ) { $vi_area = quotemeta(param('vi_area'));         } 
else { $vi_area = $vi_area;  } } else { $vi_area = quotemeta($query{'vi_area'});   }
if ( !$query{'vi_time'} )   { if ( param('vi_time')  ) { $vi_time = quotemeta(param('vi_time'));         } 
else { $vi_time = $vi_time;  } } else { $vi_time = quotemeta($query{'vi_time'});   }
if ( !$query{'vi_fanspeed'} )   { if ( param('vi_fanspeed')  ) { $vi_fanspeed = quotemeta(param('vi_fanspeed'));         } 
else { $vi_fanspeed = $vi_fanspeed;  } } else { $vi_fanspeed = quotemeta($query{'vi_fanspeed'});   }
if ( !$query{'vi_mainbrush'} )   { if ( param('vi_mainbrush')  ) { $vi_mainbrush = quotemeta(param('vi_mainbrush'));         } 
else { $vi_mainbrush = $vi_mainbrush;  } } else { $vi_mainbrush = quotemeta($query{'vi_mainbrush'});   }
if ( !$query{'vi_sidebrush'} )   { if ( param('vi_sidebrush')  ) { $vi_sidebrush = quotemeta(param('vi_sidebrush'));         } 
else { $vi_sidebrush = $vi_sidebrush;  } } else { $vi_sidebrush = quotemeta($query{'vi_sidebrush'});   }
if ( !$query{'vi_filter'} )   { if ( param('vi_filter')  ) { $vi_filter = quotemeta(param('vi_filter'));         } 
else { $vi_filter = $vi_filter;  } } else { $vi_filter = quotemeta($query{'vi_filter'});   }
if ( !$query{'vi_sensor'} )   { if ( param('vi_sensor')  ) { $vi_sensor = quotemeta(param('vi_sensor'));         } 
else { $vi_sensor = $vi_sensor;  } } else { $vi_sensor = quotemeta($query{'vi_sensor'});   }
if ( !$query{'vi_ch_count'} )   { if ( param('vi_ch_count')  ) { $vi_ch_count = quotemeta(param('vi_ch_count'));         } 
else { $vi_ch_count = $vi_ch_count;  } } else { $vi_ch_count = quotemeta($query{'vi_ch_count'});   }
if ( !$query{'vi_ch_area'} )   { if ( param('vi_ch_area')  ) { $vi_ch_area = quotemeta(param('vi_ch_area'));         } 
else { $vi_ch_area = $vi_ch_area;  } } else { $vi_ch_area = quotemeta($query{'vi_ch_area'});   }
if ( !$query{'vi_ch_time'} )   { if ( param('vi_ch_time')  ) { $vi_ch_time = quotemeta(param('vi_ch_time'));         } 
else { $vi_ch_time = $vi_ch_time;  } } else { $vi_ch_time = quotemeta($query{'vi_ch_time'});   }

# Figure out in which subfolder we are installed
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

# Save settings to config file
if (param('savedata')) {
	$conf = new Config::Simple("$home/config/plugins/$psubfolder/mi.cfg");
	if ($send_status ne 1) { $send_status = 0 }
	if ($send_consumables ne 1) { $send_consumables = 0 }
	if ($send_cleaning_history ne 1) { $send_cleaning_history = 0 }	
	$conf->param('LANGUAGE', unquotemeta($language));	
	$conf->param('LOOPTIME', unquotemeta($looptime));	
	$conf->param('UDP_PORT', unquotemeta($udp_port));
	$conf->param('SEND_CONSUMABLES', unquotemeta($send_consumables));
	$conf->param('SEND_STATUS', unquotemeta($send_status));	
	$conf->param('SEND_CLEANING_HISTORY', unquotemeta($send_cleaning_history));
	$conf->param('MI_ROBO_IP', unquotemeta($mi_robo_ip));
	$conf->param('MI_ROBO_TOKEN', unquotemeta($mi_robo_token));		
	$conf->param('VI_DND', unquotemeta($vi_dnd));	
	$conf->param('VI_SIDEBRUSH', unquotemeta($vi_sidebrush));	
	$conf->param('VI_MAINBRUSH', unquotemeta($vi_mainbrush));	
	$conf->param('VI_FILTER', unquotemeta($vi_filter));
	$conf->param('VI_SENSOR', unquotemeta($vi_sensor));	
	$conf->param('VTI_STATE', unquotemeta($vti_state));
	$conf->param('VI_STATE_CODE', unquotemeta($vi_state_code));
	$conf->param('VTI_ERROR', unquotemeta($vti_error));
	$conf->param('VI_ERROR_CODE', unquotemeta($vi_error_code));
	$conf->param('VI_BATTERY', unquotemeta($vi_battery));
	$conf->param('VI_FANSPEED', unquotemeta($vi_fanspeed));
	$conf->param('VI_AREA', unquotemeta($vi_area));
	$conf->param('VI_TIME', unquotemeta($vi_time));	
	$conf->param('VI_CH_TIME', unquotemeta($vi_ch_time));
	$conf->param('VI_CH_COUNT', unquotemeta($vi_ch_count));
	$conf->param('VI_CH_AREA', unquotemeta($vi_ch_area));
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
$send_consumables = encode_entities($conf->param('SEND_CONSUMABLES'));
$send_status = encode_entities($conf->param('SEND_STATUS'));	
$send_cleaning_history = encode_entities($conf->param('SEND_CLEANING_HISTORY'));		
$mi_robo_ip = encode_entities($conf->param('MI_ROBO_IP'));
$mi_robo_token = encode_entities($conf->param('MI_ROBO_TOKEN'));		
$vi_dnd = encode_entities($conf->param('VI_DND'));	
$vi_sidebrush = encode_entities($conf->param('VI_SIDEBRUSH'));	
$vi_mainbrush = encode_entities($conf->param('VI_MAINBRUSH'));	
$vi_filter = encode_entities($conf->param('VI_FILTER'));
$vi_sensor = encode_entities($conf->param('VI_SENSOR'));	
$vti_state = encode_entities($conf->param('VTI_STATE'));
$vi_state_code = encode_entities($conf->param('VI_STATE_CODE'));
$vti_error = encode_entities($conf->param('VTI_ERROR'));
$vi_error_code = encode_entities($conf->param('VI_ERROR_CODE'));
$vi_battery = encode_entities($conf->param('VI_BATTERY'));
$vi_fanspeed = encode_entities($conf->param('VI_FANSPEED'));
$vi_area = encode_entities($conf->param('VI_AREA'));
$vi_time = encode_entities($conf->param('VI_TIME'));
$vi_ch_time = encode_entities($conf->param('VI_CH_TIME'));
$vi_ch_count = encode_entities($conf->param('VI_CH_COUNT'));
$vi_ch_area = encode_entities($conf->param('VI_CH_AREA'));

# Set Enabled / Disabled switch
if ($send_status eq "1") {
	$Enabledstatus = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$Enabledstatus = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($send_consumables eq "1") {
	$Enabledconsumables = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$Enabledconsumables = '<option value="0" selected>off</option><option value="1">on</option>';
}
if ($send_cleaning_history eq "1") {
	$Enabledchistory = '<option value="0">off</option><option value="1" selected>on</option>';
} else {
	$Enabledchistory = '<option value="0" selected>off</option><option value="1">on</option>';
}

# Set Language
if ($language eq "de") {
	$LANGselectlist = '<option selected value="de">german</option><option value="en">english</option>\n';
} else {
	$LANGselectlist = '<option selected value="en">english</option><option value="de">german</option>\n';
}

# Title
$template_title = "MIRobo2Lox";

# Create help page
$helptext = "This is a sample short help text showed up in the right slider.";
$helptext = $helptext . "<br><br>HTML markup is <b>supported</b>.";
$helptext = $helptext . "<br><br>Maybe better to load this from a template file...";

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
