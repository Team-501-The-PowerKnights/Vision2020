clear all
close all
clc

filename = './DistanceToTy_v2.xlsx';
[num, txt, raw] = xlsread(filename);

dist = num(:,1);
angle = num(:,2);

%% quadratic
% plot(angle, dist, '*b');
p = polyfit(angle, dist, 2);
y_fit = polyval(p, angle);
plot(angle, dist, '*b');
hold on
plot(angle, y_fit, 'r--');
title('Quadratic Fit')
xlabel('Y Offset Angle (deg)')
ylabel('Distance to Target (in)')

%% linear
% figure;
% p = polyfit(angle, dist, 1);
% y_fit = polyval(p, angle);
% plot(angle, dist, '*b');
% hold on
% plot(angle, y_fit, 'r--');
% title('Linear Fit')
% xlabel('Y Offset Angle (deg)')
% ylabel('Distance to Target (in)')

%% test an individual point
% estimated_distance = polyfit(p, new_angle)
% error = actual_distance - estimated_distance
