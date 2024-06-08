% Audio settings
sampleRate = 48000;
channels = 2;
chunkSize = 1024; % Adjust based on the data rate from the bot
bitsPerSample = 16;

% Socket settings
host = 'localhost';
port = 65432;

% Create a UDP object
udpReceiver = udp(host, 'LocalPort', port, 'InputBufferSize', chunkSize * 4, 'DatagramTerminateMode', 'off');

% Open the UDP connection
fopen(udpReceiver);

% Create an audio player
audioPlayer = audioplayer(zeros(chunkSize, channels), sampleRate);

% Receive and play audio in a loop
disp('Receiving audio...');
while true
    % Read data from the UDP socket
    audioData = fread(udpReceiver, chunkSize * channels, 'int16');
    
    if ~isempty(audioData)
        % Reshape the data to match the audio channels
        audioData = reshape(audioData, chunkSize, channels);
        
        % Convert the data to double for audioplayer
        audioData = double(audioData) / (2^(bitsPerSample-1));
        
        % Play the audio
        play(audioPlayer, audioData);
    end
end