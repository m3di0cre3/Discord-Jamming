%{
udpReceiver = udpport("LocalPort", 65432);
while true
    disp(udpReceiver.NumBytesAvailable);
    receivedData = read(udpReceiver, 1024, "double");
    if ~isempty(receivedData)
        disp(['Received message: ', char(receivedData)]);
        break
    end
end
%}

audioInfo = audioinfo("twinkletwinklelittlestar.mp3");
songSampleRate = audioInfo.SampleRate;
playerSampleRate = 44100;
songWindowWidth = 1;
playerWindowWidth = 1;
songWindowLeft = 10;
playerWindowLeft = 9.8;
windowShift = 0.1;

while true
    samplesNum = [round(songWindowLeft*songSampleRate+1), round((songWindowLeft+songWindowWidth)*songSampleRate)];
    samplesNum2 = [round(playerWindowLeft*playerSampleRate+1), round((playerWindowLeft+playerWindowWidth)*playerSampleRate)];
    %disp(samplesNum)
    [stereoSong, FsSong] = audioread("twinkletwinklelittlestar.mp3", samplesNum);
    monoSong = (stereoSong(:,1) + stereoSong(:,2))/2;
    [stereoPlayer, FsPlayer] = audioread("twinkletwinklelittlestar.mp3", samplesNum2);
    monoPlayer = (stereoPlayer(:,1) + stereoPlayer(:,2))/2;
    
    [r, lags] = xcorr(monoSong, monoPlayer);
    [~, I] = max(abs(r));
    timeDiff = lags(I)/Fs;
    shiftedSongWindowLeft = songWindowLeft + timeDiff;
    [shiftedStereoSong, FsSongShifted] = audioread("twinkletwinklelittlestar.mp3", [round(shiftedSongWindowLeft*songSampleRate+1), round((shiftedSongWindowLeft+songWindowWidth)*songSampleRate)]);
    shiftedMonoSong = (shiftedStereoSong(:,1) + shiftedStereoSong(:,2))/2;
    amplitudeMultiple = sum(shiftedMonoSong)/sum(monoPlayer);
    monoPlayer = amplitudeMultiple * monoPlayer;
    
    
    comparisonSum = sqrt(mean(shiftedMonoSong-monoPlayer));


    

    disp(timeDiff)
    songWindowLeft = songWindowLeft + windowShift;
    playerWindowLeft = playerWindowLeft + windowShift;
    if (songWindowLeft+songWindowWidth)*songSampleRate > audioInfo.TotalSamples
        break
    end
end

%{

sampleRate = 48000;
channels = 2;
chunkSize = 1024; % Adjust based on the data rate from the bot
bitsPerSample = 16;

% Create a UDP object
udpReceiver = udpport("LocalPort", 12345);
while true
    disp(udpReceiver.NumBytesAvailable);
    receivedData = read(udpReceiver, 1024, "uint16");
    if ~isempty(receivedData)
        disp(['Received message: ', char(receivedData)]);
        break
    end
end

% Create an audio player
audioPlayer = audioplayer(zeros(chunkSize, channels), sampleRate);

% Receive and play audio in a loop
disp('Receiving audio...');
while true
    % Read data from the UDP socket
    audioData = read(udpReceiver, chunkSize * channels, 'int16');
    
    if ~isempty(audioData)
        % Reshape the data to match the audio channels
        audioData = reshape(audioData, chunkSize, channels);
        
        % Convert the data to double for audioplayer
        audioData = double(audioData) / (2^(bitsPerSample-1));
        
        % Play the audio
        xcorr(, audioData)
    end
end
%}

function pauses(delay,t0)

persistent sys_delay;

if nargin<2
   t0=tic;
end

if isempty(sys_delay)
   %%
   sys_delay = 0;
   % Use this function itself to calibrate system delays on its first call   
   N=66; delay=0.002+0.002*rand(1,N); % use approx. 0.2 sec on first call
   %N=333; delay=0.002+0.002*rand(1,N); % use approx. 1 sec on first call
   dt=zeros(1,N);
   pauses(0); % JIT initialization
   for k=1:N
      t1=tic; pauses(delay(k),t1); dt(k)=toc(t1);
   end
   dt = (dt-delay);   
   sys_delay = mean(dt);
end

if 0 % enable to use pause() instead of java.lang.Thread.sleep()
   sys_step = 0.015; % ~ 3 sigma accuracy of pause()
   if delay - toc(t0) > 3*sys_step
      pause(delay - toc(t0) - 2*sys_step); % this will realy stop Matlab
   end
else
   sys_step = 0.002; % ~ 6 sigma accuracy of java.lang.Thread.sleep()
   if delay - toc(t0) > 3*sys_step
      java.lang.Thread.sleep((delay - toc(t0) - 2*sys_step)*1000); % this will realy stop Matlab
   end
end
while delay - toc(t0) > sys_delay
   % Do nothing...
end
return
end
%}