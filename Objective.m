function phi = Objective()
    %%* Section contains code for setting up of Mass-inertia tensor.
    mass_data = readmatrix('./Data/engineParams.csv');
    mass = mass_data(1,1);           % Reads Engine mass in KG from the file.
    principalMoments = mass_data(:,2);  % Reads given moments

    % Represented in the Eigenspace of principal moments
    Moments = [principalMoments(1) 0 0; 0 principalMoments(2) 0; 0 0 principalMoments(3)];

    % Transformation Matrix.
    R = mass_data(:,3:5);
    theta = deg2rad(mass_data(:,6));

    R_x = [1,0,0; 0, cos(theta(1)), -sin(theta(1)); 0, sin(theta(1)), cos(theta(1))];
    R_y = [cos(theta(2)), 0, sin(theta(2)); 0,1,0; -sin(theta(2)), 0, cos(theta(2))];
    R_z = [cos(theta(3)), -sin(theta(3)), 0; sin(theta(3)), cos(theta(3)), 0; 0,0,1];

    Moments = R'*Moments*R; % Converts from principal moment coordinates to global coordinates.
    Moments = R_z*Moments*R_z';
    Moments = R_y*Moments*R_y';
    Moments = R_x*Moments*R_x';


    M = Mass(mass, Moments);    % Sets M to final value of mass-inertia tensor

    %%* Section contains code for setting up of mounts.
    % Since no orientations are provided, assuming the following:
    mount1_data = readmatrix('./Data/mount1.csv');
    mount1 = struct;                        % Declares each mount as a struct
    mount1.k = mount1_data(:,2)';           % Sets directional stress values in order x, y, z.
    mount1.eta = mount1_data(:,3)';         % Sets damping in order x, y, z.
    mount1.position = mount1_data(:,7)';    % Sets position in global coordinates in order x, y, z.
    mount1.transform = mount1_data(:,4:6);

    % Same description as above.
    mount2_data = readmatrix('./Data/mount2.csv');
    mount2 = struct;
    mount2.k = mount2_data(:,2)';
    mount2.eta = mount2_data(:,3)';
    mount2.position = mount2_data(:,7)';
    mount2.transform = mount2_data(:,4:6);

    mount3_data = readmatrix('./Data/mount3.csv');
    mount3 = struct;
    mount3.k = mount3_data(:,2)';
    mount3.eta = mount3_data(:,3)';
    mount3.position = mount3_data(:,7)';
    mount3.transform = mount3_data(:,4:6);

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

    force_data = readmatrix('./Data/forces.csv');

    fundamental = 194;      % Angular frequency.

    for i = 1:size(force_data(:,1))
        forces = [forces; Perturbation(force_data(i,1), force_data(i,2), force_data(i,3), force_data(i,4))];
    end

    %%* Calculating the displacement phasor:
    U = Phasor(K, M, forces, fundamental);

    F_1 = K_1*(G_1*U);
    F_2 = K_2*(G_2*U);
    F_3 = K_3*(G_3*U);

    phi = (max(real(F_1(1,:))))^2 + (max(real(F_1(2,:))))^2 + (max(real(F_1(3,:))))^2;
    phi = phi + (max(real(F_2(1,:))))^2 + (max(real(F_2(2,:))))^2 + (max(real(F_2(3,:))))^2;
    phi = phi + (max(real(F_3(1,:))))^2 + (max(real(F_3(2,:))))^2 + (max(real(F_3(3,:))))^2;
    phi = phi^0.5;
end