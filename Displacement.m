%%* Section clears terminal and workspace.
clear;
clc;

%%* Section contains code for setting up of Mass-inertia tensor.
mass = 170;                     % Engine Mass is given to be 170 kg
principalMoments = [4, 10, 8];  % Given Moments

% Represented in the Eigenspace of principal moments
Moments = [principalMoments(1) 0 0; 0 principalMoments(2) 0; 0 0 principalMoments(3)];

% ? I am not sure if the transformation matrix given below is correct.
R =    [cos(deg2rad(5)) cos(deg2rad(12.3)) cos(deg2rad(-20.7))];
R = [R; cos(deg2rad(5)) cos(deg2rad(12.3)) cos(deg2rad(-20.7))];
R = [R; cos(deg2rad(5)) cos(deg2rad(12.3)) cos(deg2rad(-20.7))];

Moments = R'*Moments*R; % Converts from principal moment coordinates to global coordinates.

M = Mass(mass, Moments);    % Sets M to final value of mass-inertia tensor

%%* Section contains code for setting up of mounts.
% Since no orientations are provided, assuming the following:
mount1 = struct;                            % Declares each mount as a struct
mount1.k = [10^5 10^5 10^5];                % Sets directional stress values in order x, y, z.
mount1.eta = [0.1 0.1 0.1];                 % Sets damping in order x, y, z.
mount1.position = [-0.25 0.25 -0.25];       % Sets position in global coordinates in order x, y, z.
mount1.transform = eye(3);                  % ? Transformation matrix to describe rotational orientation.
                                            % ? Currently set to [I] because no angles have been provided.
% Same description as above.
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

%%* Generating the Stress tensors in global coordinates.
K_1 = Stress(mount1);
K_2 = Stress(mount2);
K_3 = Stress(mount3);

%%* Generating the G Transforms:
G_1 = G(mount1);
G_2 = G(mount2);
G_3 = G(mount3);

%%* Generating K:
K = zeros(6,6);

% Applying G transforms
K = K + G_1'*K_1*G_1;
K = K + G_2'*K_2*G_2;
K = K + G_3'*K_3*G_3;

%%* Defining list of forces and moments:
forces = [];
moments = [];

forces = [forces Perturbation(220, 194, -3, 'z')];
forces = [forces Perturbation(33, 388, 0.35, 'z')];
moments = [moments Perturbation(85, 194, 1.8, 'x')];
moments = [moments Perturbation(44, 388, 1.6, 'x')];
moments = [moments Perturbation(15, 582, 1.5, 'x')];
moments = [moments Perturbation(19.8, 194, 3.0, 'y')];
moments = [moments Perturbation(2.9, 388, 0.35, 'y')];

%%* Calculating the displacement phasor:
U = Phasor(K, M, forces, moments);