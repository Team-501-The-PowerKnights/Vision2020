function y_calculated = findDistance(a1, angle, h1, h2)
    y_calculated = zeros(length(angle), 1);
    for i = 1:length(angle)
        y_calculated(i) = (h2 - h1) / tand(a1 + angle(i));
    end
end