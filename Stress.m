function K = Stress(mount)
    % Function takes in a mount struct.
    % RETURNS: Its computed stress tensor, K, in global coordinates.

    K = eye(3);

    for i = 1:3

        % Each diagonal entry of the local coordinate stress tensor is generated.
        K(i,i) = K(i,i) * mount.k(i)*(1 + mount.eta(i)*1i); 
    end
    
    % Local coordinate stress tensor is transformed into global coordinates.
    K = (mount.transform)'* K *(mount.transform);
end