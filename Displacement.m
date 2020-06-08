clear;
clc;

mass = 170;                     % Engine Mass is given to be 170 kg
principalMoments = [4, 10, 8];  % Given Moments
Moments = [principalMoments(1) 0 0; 0 principalMoments(2) 0; 0 0 principalMoments(3)];   % Represented in the Eigenspace of principal moments

% I am not sure if the transformation matrix given below is correct.
R = [cos(deg2rad(5)) cos(deg2rad(5)) cos(deg2rad(5)); cos(deg2rad(12.3)) cos(deg2rad(12.3)) cos(deg2rad(12.3)); cos(deg2rad(-20.7)) cos(deg2rad(-20.7)) cos(deg2rad(-20.7))];  % Direction cosines implemented into transformation.

Moments = R*Moments*R'; % Converts from principal moment coordinates to global coordinates.

M = Mass(mass, Moments);    % Sets M to final value.

% Since no orientations are provided, assuming the following:
mount1 = struct;
mount1.k = [10^5 10^5 10^5];
mount1.eta = [0.1 0.1 0.1];
mount1.position = [-0.25 0.25 -0.25];
mount1.transform = eye(3);

mount2 = struct;
mount2.k = [10^5 10^5 10^5];
mount2.eta = [0.1 0.1 0.1];
mount2.position = [0.30 -0.10 0.05];
mount2.transform = eye(3);

mount3 = struct;
mount3.k = [10^5 10^5 10^5];
mount3.eta = [0.1 0.1 0.1];
mount3.position = [-0.35 -0.35 -0.35];
mount3.transform = eye(3);

% Generating the Stress tensors.
K_1 = Stress(mount1.k, mount1.eta, mount1.transform);
K_2 = Stress(mount2.k, mount2.eta, mount2.transform);
K_3 = Stress(mount3.k, mount3.eta, mount3.transform);

% Generating the G Transforms:
G_1 = G(mount1.position);
G_2 = G(mount2.position);
G_3 = G(mount3.position);

% Generating K:
K = zeros(6,6);
K = K + G_1'*K_1*G_1;
K = K + G_2'*K_2*G_2;
K = K + G_3'*K_3*G_3;

forces = [];
moments = [];

% Forces and moments:
forces = [forces Perturbation(220, 194, -3, 'z')];
forces = [forces Perturbation(33, 388, 0.35, 'z')];
moments = [moments Perturbation(85, 194, 1.8, 'x')];
moments = [moments Perturbation(44, 388, 1.6, 'x')];
moments = [moments Perturbation(15, 582, 1.5, 'x')];
moments = [moments Perturbation(19.8, 194, 3.0, 'y')];
moments = [moments Perturbation(2.9, 388, 0.35, 'y')];

% Calculating the displacement phasor:
U = Phasor(K, M, forces, moments);