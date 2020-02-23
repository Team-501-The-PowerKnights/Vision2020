clear all
close all
clc

filename = './DistanceToRPM.xlsx';
[num, txt, raw] = xlsread(filename);

dist = num(:,1);
rpm = num(:,2);

%% quadratic
% plot(rpm, dist, '*b');
p = polyfit(dist, rpm, 2);
y_fit = polyval(p, dist);
plot(dist, rpm, '*b');
hold on
plot(y_fit, rpm, 'r--');
title('Quadratic Fit')
xlabel('Y Offset rpm (deg)')
ylabel('Distance to Target (in)')

%% linear
% figure;
% p = polyfit(dist, rpm, 1);
% y_fit = polyval(p, dist);
% plot(dist, rpm, '*b');
% hold on
% plot(y_fit, rpm, 'r--');
% title('Linear Fit')
% xlabel('Y Offset rpm (deg)')
% ylabel('Distance to Target (in)')

%% test an individual point
% estimated_distance = polyval(p, new_dist)
% error = actual_distance - estimated_distance
