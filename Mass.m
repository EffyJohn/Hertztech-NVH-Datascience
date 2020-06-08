function M = Mass(mass, Moments)
    M = [mass*eye(3), zeros(3,3); zeros(3,3), Moments];
end

