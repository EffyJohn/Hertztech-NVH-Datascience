function K = Stress(k_i, eta_i, T)
    K = eye(3);
    for i = 1:3
        K(i,i) = K(i,i) * k_i(i)*(1+eta_i(i)*1i);
    end
    
    K = T'*K*T;
end