function G = G(coordinates)
    G = zeros(3,3);
    
    G(1,2) = coordinates(3);
    G(1,3) = -1*coordinates(2);
    G(2,3) = coordinates(1);
    
    G = G + (G'*-1);
    
    G = [eye(3), G];
end