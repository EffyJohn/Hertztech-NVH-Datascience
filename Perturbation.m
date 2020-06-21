function perturbation = Perturbation(amplitude, frequency, phase, phasorAxis)
    % Takes parameters of a perturbation phasor as inputs.
    % RETURNS: One struct that contains all the perturbation data encapsulated.
    % TODO: Replace this function with a perturbation class, and make this its constructor.
    perturbation = struct;
    perturbation.amplitude = amplitude;
    perturbation.frequency = frequency;
    perturbation.phase = phase;
    perturbation.axis = phasorAxis;
end