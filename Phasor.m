function U = Phasor(K, M, forces, fundamental)
    
    % Set Sampling frequency. Default is 20 times max frequency.
    samplingFrequency = ((fundamental*3)*20)/(2*pi);

    % Calculate time period of one cycle.
    timePeriod = (fundamental/(2*pi))^(-1);

    % Create sample times for thrice the length of one period
    time = 0:samplingFrequency^(-1):timePeriod*3;

    U = [0; 0; 0; 0; 0; 0];

    % Create sample vector that is used to generate force phasors
    U = U*time;

    % Generate all phasors, and calculate final displacement.
    for index = 1:size(forces)
        forces(index).phasor = forces(index).frequency*time;
        forces(index).phasor = forces(index).phasor + forces(index).phase;
        forces(index).phasor = forces(index).phasor*1i;
        forces(index).phasor = exp(1).^forces(index).phasor;
        forces(index).phasor = forces(index).phasor*forces(index).amplitude;
        
        temp = [0; 0; 0; 0; 0; 0];
        temp(forces(index).axis) = 1;

        forces(index).phasor = temp*forces(index).phasor;

        inverse = K - M*(forces(index).frequency^2);
        inverse = inverse^-1;

        U = U + inverse*forces(index).phasor;
    end
end

