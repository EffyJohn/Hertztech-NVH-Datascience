function M = Mass(mass, Moments)
    % Function takes in one value in Kg for mass, and
    % a row vector containing the three principal inertias.
    % RETURNS: M, which is the mass-inertia tensor.
     
    M = [mass*eye(3), zeros(3,3); zeros(3,3), Moments];
end

