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
plot(dist, y_fit, 'r--');
title('Quadratic Fit')
xlabel('Distance (in)')
ylabel('RPM')

%% linear
% figure;
% p = polyfit(dist, rpm, 1);
% y_fit = polyval(p, dist);
% plot(dist, rpm, '*b');
% hold on
% plot(dist, y_fit, 'r--');
% title('Linear Fit')
% xlabel('Distance (in)')
% ylabel('RPM')

%% test an individual point
% estimated_rpm = polyval(p, new_dist)
% error = actual_rpm - estimated_rpm
