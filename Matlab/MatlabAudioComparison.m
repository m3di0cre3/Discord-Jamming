
port = 12346;

t = tcpserver('0.0.0.0', port, 'ByteOrder', 'little-endian');

% Display server information
disp('Server is waiting for a connection...');

audioInfo = audioinfo("cmajorscale.mp3");
songSampleRate = audioInfo.SampleRate;
playerSampleRate = 44100;
songWindowWidth = 1;
playerWindowWidth = 1;
songWindowLeft = 10;
playerWindowLeft = 10;
windowShift = 0.1;
playerAudioVector = zeros(44100, 1);
posInPlayerAudioVector = 1;
processedData = zeros(1470, 1);

while true
    samplesNum = [round(songWindowLeft*songSampleRate+1), round((songWindowLeft+songWindowWidth)*songSampleRate)];
    samplesNum2 = [round(playerWindowLeft*playerSampleRate+1), round((playerWindowLeft+playerWindowWidth)*playerSampleRate)];
    %disp(samplesNum)
    [stereoSong, FsSong] = audioread("cmajorscale.mp3", samplesNum);
    monoSong = (stereoSong(:,1) + stereoSong(:,2))/2;
    while posInPlayerAudioVector < 44100
        while t.NumBytesAvailable == 0
        end
        %disp(t.NumBytesAvailable)
        newData = read(t, t.NumBytesAvailable);
        for i = 1:1470
            processedData(i) = typecast(uint8([newData(i*4-3), newData(i*4-2), newData(i*4-1), newData(i*4)]), "single");
        end
        
        %disp(class(processedData))
        %disp(processedData)
        playerAudioVector(posInPlayerAudioVector:posInPlayerAudioVector+1469) = processedData;
        posInPlayerAudioVector = posInPlayerAudioVector + 1470;
        %disp('Data received:');
        %disp(data);
    end

    [r, lags] = xcorr(monoSong, playerAudioVector);
    [~, I] = max(abs(r));
    timeDiff = lags(I)/FsSong;
    shiftedSongWindowLeft = songWindowLeft + timeDiff;
    [shiftedStereoSong, FsSongShifted] = audioread("cmajorscale.mp3", [round(shiftedSongWindowLeft*songSampleRate+1), round((shiftedSongWindowLeft+songWindowWidth)*songSampleRate)]);
    shiftedMonoSong = (shiftedStereoSong(:,1) + shiftedStereoSong(:,2))/2;
    amplitudeMultiple = sum(shiftedMonoSong)/sum(playerAudioVector);
    playerAudioVector = amplitudeMultiple * playerAudioVector;
    
    
    comparisonSum = sqrt(sqrt(sqrt(sqrt(abs(mean(shiftedMonoSong-playerAudioVector))))));
    if shiftedSongWindowLeft > 10
        disp([shiftedMonoSong, playerAudioVector])
    end

    songWindowLeft = songWindowLeft + windowShift;
    playerWindowLeft = playerWindowLeft + windowShift;
    if (songWindowLeft+songWindowWidth)*songSampleRate > audioInfo.TotalSamples
        break
    end
    playerAudioVector = vertcat(playerAudioVector(4411:44100), zeros(4410, 1));
    posInPlayerAudioVector = 39691; 
end
