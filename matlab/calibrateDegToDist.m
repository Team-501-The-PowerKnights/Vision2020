clear all
close all
clc

filename = './DistanceToTy_v2.xlsx';
[num, txt, raw] = xlsread(filename);

dist = num(:,1);
angle = num(:,2);

% angle of camera relative to ground
a1 = 7.3;
% height of camera from ground
h1 = 36.875;
% height of center of target from ground
h2 = 89.75;
%% quadratic
% plot(angle, dist, '*b');
p = polyfit(angle, dist, 2);
y_fit = polyval(p, angle);
calculated_dist = findDistance(a1, angle, h1, h2);
plot(angle, dist, '*b');
hold on
plot(angle, y_fit, 'r-');
plot(angle, calculated_dist, 'g-')
title('Estimating Distance from Y Offset Angle')
legend('Measured points', 'Quadratic Fit', 'Distance From Trigonometry')
xlabel('Y Offset Angle (deg)')
ylabel('Distance to Target (in)')

%% calculate error
quadratic_error = dist - y_fit;
max_quadratic_error = max(abs(quadratic_error));
min_quadratic_error = min(abs(quadratic_error));
avg_quadratic_error = mean(abs(quadratic_error));

disp('Stats on the error from curve fitting');
fprintf('The average error was %f\n', avg_quadratic_error);
fprintf('The min error for a data point was %f\n', min_quadratic_error);
fprintf('The max error for a data point was %f\n\n\n', max_quadratic_error);

trig_error = dist - calculated_dist;
max_trig_error = max(abs(trig_error));
min_trig_error = min(abs(trig_error));
avg_trig_error = mean(abs(trig_error));

disp('Stats on the error from calculating distance using trigonometry');
fprintf('The average error was %f\n', avg_trig_error);
fprintf('The min error for a data point was %f\n', min_trig_error);
fprintf('The max error for a data point was %f\n', max_trig_error);


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
% estimated_distance = polyval(p, new_angle)
% error = actual_distance - estimated_distance
