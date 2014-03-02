#! /usr/bin/perl

# Fibonacci generator using dynamic programming

use warnings;
use strict;

my $num="";
do {
	print("Please enter a number\n");
	$num = <STDIN>;
	chomp($num);
} while (!($num =~ m/^[0-9]+$/));

print("Computing $num terms of Fibonacci sequence:\n");

my @array;
$array[0] = 0;
$array[1] = 1;

my $index = 0;

for (my $i=0; $i < $num; $i++) {
	$index = ($i+1)%2;
	print("$array[($i+1)%2] ");
	$array[$i%2] = $array[0] + $array[1];
}
print("\n");
