function G = G(mount)
    % Takes a mount as input.
    % RETURNS: The G matrix-transform based on its position.

    G = zeros(3,3);

    % Fill upper triangle of the cap section of the matrix.
    G(1,2) = mount.position(3);
    G(1,3) = -1*mount.position(2);
    G(2,3) = mount.position(1);
    
    % Using the skew-symmetry of the cap section to generate lower triangle.
    G = G + (G'*-1);
    
    % Appends above created skew-symmetric cap matrix to an identity matrix.
    G = [eye(3), G];
end