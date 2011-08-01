#!/usr/bin/perl
{
	local $/=undef;
	open FILE, '/proc/acpi/battery/BAT0/state' or die $!;
	binmode FILE;
	$info = <FILE>;
}
$info =~ /present rate:\s+(\d+) \w+\s*\n*remaining capacity:\s+(\d+)/m;
$rate, $remaining = $1, $2;
if( $info =~ /charged/ or $2 == 0) {
	print "charged"
}
else {
	$remaining_time = $2/$1;
	$hours = int($remaining_time);
	$minutes = sprintf("%02d", int(($remaining_time - $hours)*60));
	if($info =~ /discharging/) {
		print "$hours:$minutes";
	}
	else {
		print "($hours:$minutes)";
	}
}
