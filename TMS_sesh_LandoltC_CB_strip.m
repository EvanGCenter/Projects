% Cortical Transmission time study script
% created by Evan Center
% aid from Kyle Mathewson, John Clevenger, Ramisha Knight & Diane Beck
% UIUC
% last updated November 2016
% MUST LOAD VARIABLES FROM TRAINING MODE TO FUNCTION

% close all
% sca;

load phase2_photometry %load gamma correction and reset parameters
load endCLUT
 
date_ran = clock'; %marks date and time of start of experiment

%Screen('Preference','SuppressAllWarnings',1); %supresses mild level warnings, some stuff still comes up that I don't understand currently
KbName('UnifyKeyNames'); %unifies keynames across different OSs
rng('shuffle'); %sets new base for random number generator by using current time

%% Subject and screen parameters section
%Sets the units of your root object (screen) to pixels
set(0,'units','pixels');  
%Obtains this pixel information
Pix_SS = get(0,'screensize');
CM_SS = [0 0 37 28]; %DOIL monitor is 38w x 29h

ppcm_x = Pix_SS(3)/CM_SS(3); % pixels per horizontal centimeter

view_distance = 90; %standard viewing distance of 57 cm allows 1 degree = 1 cm

%size_at_fix = .0901; %size of target at fixation in degrees, from Railo & Koivisto
%size_at_fix = .175; %size of target at fixation in degrees, from Tapia & Beck 2014
%size_at_fix = .3726; %from Kelly et al. 2008
size_at_fix = .56627; 

%% Spatial frequency calculations for stimuli
cmpd = 2*(tan(deg2rad(0.5)*view_distance)); %cm per degree
PPD = ppcm_x*cmpd; %pixels per degree

%% TMS junk
DEBUG = input('debug? ');

if DEBUG == 0
    % Set up parallel port
    % initialize the inpoutx64 low-level I/O driver
    config_io;
    % optional step: verify that the inpoutx64 driver was successfully installed
    global cogent;
    if( cogent.io.status ~= 0 )
        error('inp/outp installation failed');
    end
    % write a value to the default LPT1 printer output port (at 0x378)
    address = hex2dec('378');
    outp(address,0);  %set pins to zero
end

if DEBUG == 1
    Screen('Preference', 'SkipSyncTests', 0);
end

% Screen('Preference', 'SkipSyncTests', 0);

%% More setup stuff
subj_num = input('Please enter subject number: '); %prompt for subject #

fix_color = [0 0 155]; %set fixation color to black
back_color = [255/2 255/2 255/2]; %set background color to medium gray

n_blocks = 24; %number of blocks
n_TpB = 32; %number of trials per block
n_tot_trials = n_blocks*n_TpB; %total number of trials

screenNumber = max(Screen('Screens'));  %get the maximum screen number i.e. get an external screen if avaliable
[window,rect] = Screen('OpenWindow',screenNumber,back_color,[],32,2);  %opens a window,  monitor, with gray background, with dimensions
Priority(1);
originalCLUT=Screen('LoadNormalizedGammaTable',window,inverseCLUT);
% 
smlchckr = imread('smlchckr.jpg'); %load checkerboard texture
texture = Screen('MakeTexture',window,smlchckr);
% 
font_size = 20; %create font size variable
[center(1),center(2)] = WindowCenter(window); %locates center
fixation = [center(1) center(2)]; %create fixation variable
Screen('TextSize',window,font_size); %Set the font size
Screen('TextFont', window,'Calibri'); %Set the font

refresh = Screen('GetFlipInterval',window);  %refresh period in seconds
slack = refresh/2; %compute slack to keep timing

% TMS lag values: 15 lags in steps of refresh rate
counter = 0:15;
TMS_lags = refresh.*counter;
ZZ = length(TMS_lags); % shorthand for calcs
TMS_lag_order = repmat(TMS_lags,n_tot_trials/ZZ,1); %repeats the matrix to result in a lag for every trial
TMS_lag_order = reshape(TMS_lag_order,n_tot_trials,1);

%definitions of keys
left_key = KbName('LeftArrow');
right_key = KbName('RightArrow');
up_key = KbName('UpArrow');
down_key = KbName('DownArrow');
target_key = KbName('left_mouse');
HideCursor;

%% stim parameters
norm = repmat(back_color,n_tot_trials,1);
color = norm(randperm(end),:);

sc1 = round((pixels*.6)/2); %for radius of inner opening of Landolt C
%sc2 = round((pixels*.2)/2); %keep gap size from training
sc3 = round(pixels/2); %for radius of Landolt C

outerT = [x_avg-sc3,y_avg-sc3,x_avg+sc3,y_avg+sc3]; %outer circle, target
outerM = [x_mirror-sc3,y_mirror-sc3,x_mirror+sc3,y_mirror+sc3]; %outer circle, mirror
innerT = [x_avg-sc1,y_avg-sc1,x_avg+sc1,y_avg+sc1]; %inner opening, target
innerM = [x_mirror-sc1,y_mirror-sc1,x_mirror+sc1,y_mirror+sc1]; %inner opening, mirror
gapRT = [x_avg,y_avg-sc2,x_avg+sc3,y_avg+sc2]; %all possible landolt c gaps
gapRM = [x_mirror,y_mirror-sc2,x_mirror+sc3,y_mirror+sc2];
gapLT = [x_avg-sc3,y_avg-sc2,x_avg,y_avg+sc2];
gapLM = [x_mirror-sc3,y_mirror-sc2,x_mirror,y_mirror+sc2];
gapUT = [x_avg-sc2,y_avg-sc3,x_avg+sc2,y_avg];
gapUM = [x_mirror-sc2,y_mirror-sc3,x_mirror+sc2,y_mirror];
gapDT = [x_avg-sc2,y_avg,x_avg+sc2,y_avg+sc3];
gapDM = [x_mirror-sc2,y_mirror,x_mirror+sc2,y_mirror+sc3];

gaps = [gapRT;gapDT;gapLT;gapUT];

%lump together to make full stims
targ_R = [outerT innerT gapRT];
targ_L = [outerT innerT gapLT];
targ_U = [outerT innerT gapUT];
targ_D = [outerT innerT gapDT];
mirr_R = [outerM innerM gapRM];
mirr_L = [outerM innerM gapLM];
mirr_U = [outerM innerM gapUM];
mirr_D = [outerM innerM gapDM];

f = ceil(sqrt(((pixels/7)^2)+((pixels/7)^2)));

%further lumping
targz = [targ_R;targ_L;targ_U;targ_D];
targz = repmat(targz,(n_tot_trials/length(targz(:,1)))/32,1);
mirrz = [mirr_R;mirr_L;mirr_U;mirr_D];
mirrz = repmat(mirrz,(n_tot_trials/length(mirrz(:,1)))/32,1);
stimi = [targz;mirrz];
stimi = repmat(stimi,16,1);

%counterbalance all the stim types across lags
CB_mat = [TMS_lag_order,stimi];
CB_order = CB_mat(randperm(end),:);

TMS_lag_current = CB_order(:,1);
stimi = CB_order(:,2:13);

%use random pieces of the checkerboard for texturing
chck_spc = NaN(n_tot_trials,4);
for s = 1:n_tot_trials
    spot = randi([0+round(pixels),800-round(pixels)]);
    chck_spc(s,:) = [spot-sc3,spot-sc3,spot+sc3,spot+sc3];
end

gExposure = (refresh*2); %exposure duration of stimuli, aligned with refresh rate; ends up being 3 frames w/ flip

%% instructions
Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
Screen('DrawText',window,'Hi! Here are your instructions.',5,fixation(2)-160,fix_color);
Screen('DrawText',window,'On each trial, you will see a C shape such as that shown below.',5,fixation(2)-130,fix_color);
Screen('DrawText',window,'Press any button to continue with instructions',5,fixation(2)-100,fix_color);
Screen('DrawTexture',window,texture,chck_spc(1,:),outerT);
Screen('FrameOval',window,back_color,[outerT(1)-f,outerT(2)-f,outerT(3)+f,outerT(4)+f],f,f);
Screen('FillOval',window,back_color,innerT);
Screen('FillRect',window,back_color,gapRT);    
Screen('Flip',window);
WaitSecs(1);
KbPressWait; %wait for subject to press button

%show the instructions
ready = 0;
begin = KbName('Return');
while ready ~= 1
for g = 1:size(gaps,1)
Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
Screen('DrawText',window,'Your task is to indicate the direction of the C shape.',5,fixation(2)-160,fix_color);
Screen('DrawText',window,'Use the arrow to keys to indicate your response on each trial.',5,fixation(2)-130,fix_color);
Screen('DrawText',window,'Please respond as quickly and accurately as possible.',5,fixation(2)-100,fix_color);
Screen('DrawText',window,'When you are ready, press and hold "Enter" to begin the experiment.',5,fixation(2)-70,fix_color);  %Display instructions
Screen('DrawTexture',window,texture,chck_spc(1,:),outerT);
Screen('FrameOval',window,back_color,[outerT(1)-f,outerT(2)-f,outerT(3)+f,outerT(4)+f],f,f);
Screen('FillOval',window,back_color,innerT);
Screen('FillRect',window,back_color,gaps(g,:));    
Screen('Flip',window);
WaitSecs(3/4);
[keyIsDown,secs,keyCode] = KbCheck;
if keyCode(begin)
    ready = 1;
    break
end
end
end

Screen('Flip',window);
WaitSecs(1);

% setting up a series of directories for data
trial_start = NaN(n_tot_trials,1); %when the trial begins
trial_end =  NaN(n_tot_trials,1); %when the trial ends
TMS_onset = NaN(n_tot_trials,1); %time stamps for TMS onset
stim_start = NaN(n_tot_trials,1); %stimulus onset times
stim_end = NaN(n_tot_trials,1); %stimulus offset times
resp_start = NaN(n_tot_trials,1); %marks beginning of response window
response_code = NaN(n_tot_trials,1); %responses, 1 for correct 0 for incorrect
response_time = NaN(n_tot_trials,1); %time of response
wait_time = NaN(n_tot_trials,1); %wait time between trials

%% experimental trials section
for i = 1:n_tot_trials
    
    if mod(i,n_TpB) == 1
        WaitSecs(1);
    end
    
    %draws fixation and waits a random amount of time between 1.5 and 3 s
    Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
    Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
    Screen('Flip',window); %print fixation
    %counter below and seen throughout makes for accurate trial counting
    trial_start(i) = GetSecs(); %note beginning of trial
    WaitSecs(randi([1500,3000])/1000); %delay to stim onset
    wait_time(i) = GetSecs() - trial_start(i);
    
    %flashes a (pseudo)random stimulus at target or mirror location for 3 frames
    Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
    Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
    Screen('DrawTexture',window,texture,chck_spc(i,:),stimi(i,1:4));
    Screen('FrameOval',window,back_color,[stimi(i,1)-f,stimi(i,2)-f,stimi(i,3)+f,stimi(i,4)+f],f,f);
    Screen('FillOval',window,back_color,stimi(i,5:8));
    Screen('FillRect',window,back_color,stimi(i,9:12));    
    Screen('Flip',window);
    
    stim_start(i) = GetSecs() - trial_start(i);
    
    if DEBUG == 0
        if TMS_lag_current(i) <= gExposure
            %in blocks where TMS lag is shorter than or equal to stim exposure
            %duration, wait for the whole lag then add the remaining stim
            %exposure time to have normal stim duration
            WaitSecs(TMS_lag_current(i)-.001);
            %200 + TMS lag marks TMS pulse in EEG
            outp(address,200);
            %notes TMS onset in data
            TMS_onset(i) = GetSecs() - trial_start(i);
            WaitSecs(.001);
            outp(address,0);
            WaitSecs((gExposure)-TMS_lag_current(i));
            Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
            Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
            Screen('Flip',window,[],0);
            %stim offsets
            stim_end(i) = GetSecs()-trial_start(i);
        
        else
            WaitSecs(gExposure); %for lags longer than exposure duration, show the stim then deliver TMS pulse        
            Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
            Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
            Screen('Flip',window);
            %stim offsets
            stim_end(i) = GetSecs()-trial_start(i);
            WaitSecs(TMS_lag_current(i)-(gExposure+refresh));
            outp(address,200);
            TMS_onset(i) = GetSecs() - trial_start(i);
            %WaitSecs(.001);
            outp(address,0);
        end
    elseif DEBUG == 1
        %do this if not hooked up to TMS
        WaitSecs(gExposure);
        Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
        Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
        Screen('Flip',window,[],0);
        stim_end(i) = GetSecs()-trial_start(i);
    end
    
    %displays fixation again
    Screen('DrawLine',window,fix_color,fixation(1),fixation(2)-5,fixation(1),fixation(2)+5,2);    
    Screen('DrawLine',window,fix_color,fixation(1)-5,fixation(2),fixation(1)+5,fixation(2),2);
    Screen('Flip',window);
    
    %notes beginning of response window, does response stuff
    resp_start(i) = GetSecs() - trial_start(i); %starts tracking time at each trial start
    [secs,keyCode] = KbPressWait; %take note of which key was pressed when
    
    response_code(i) = find(keyCode); 
    response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
         
    %notes trial end
    trial_end(i) = GetSecs() - trial_start(i);

    if mod(i,n_TpB) == 0
        
        i_b = i/n_TpB;
        %displays inter-block instructions, counter for sanity
        countstr = num2str(i_b);
        blockstr = num2str(n_blocks);
        message = ['You have completed block ', countstr, ' out of ', blockstr];
        WaitSecs(1);

        if i_b == n_blocks %final instructions
            Screen('DrawText',window,'You have completed the experiment! Thanks for participating!',5,fixation(2)-100,fix_color);
            Screen('DrawText',window,'Please call the experimenter',5,fixation(2)-70,fix_color);
            Screen('Flip',window);
            WaitSecs(2);
            KbPressWait; %wait for subject to press button
        elseif mod(i_b,4) == 0 %change TMS coil
            Screen('DrawText',window,message,5,fixation(2)-130,fix_color);
            Screen('DrawText',window,'Please call the experimenter to adjust the equipment',5,fixation(2)-100,fix_color);
            Screen('Flip',window);
            WaitSecs(10);
            KbPressWait;
        else %interblock instructions
            Screen('DrawText',window,message,5,fixation(2)-160,fix_color);
            Screen('DrawText',window,'You may now take a quick break.',5,fixation(2)-130,fix_color);
            Screen('DrawText',window,'Thanks for the help! When you are ready, press any button',5,fixation(2)-100,fix_color);
            Screen('DrawText',window,'to continue to the next block.',5,fixation(2)-70,fix_color);
            Screen('Flip',window);
            WaitSecs(2);
            KbPressWait; %wait for subject to press button
        end
    end
end

response = NaN(n_tot_trials,1);

for i = 1:n_tot_trials
   
    if stimi(i,9:12) == gapRT(1,:)
        if response_code(i) == 39
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    elseif stimi(i,9:12) == gapRM(1,:)
        if response_code(i) == 39
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    elseif stimi(i,9:12) == gapLT(1,:)
        if response_code(i) == 37
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    elseif stimi(i,9:12) == gapLM(1,:)
        if response_code(i) == 37
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    elseif stimi(i,9:12) == gapUT(1,:)
        if response_code(i) == 38
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    elseif stimi(i,9:12) == gapUM(1,:)
        if response_code(i) == 38
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    elseif stimi(i,9:12) == gapDT(1,:)
        if response_code(i) == 40
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    elseif stimi(i,9:12) == gapDM(1,:)
        if response_code(i) == 40
            response(i) = 1; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        else response(i) = 0; 
            response_time(i) = (GetSecs() - trial_start(i)) - resp_start(i);
        end
    end
end

%% clean up, end
%calculate actual observed stim time and TMS lags for data    
stim_time = stim_end-stim_start;
TMS_LAG_OBS = TMS_onset-stim_start;    
accuracy = mean(response); %calculates overall accuracy ignoring cases of mutlitple button presses in a trial
mean_response_time = nanmean(response_time); %calculates average response time ignoring correct rejections on catch trials
error = TMS_LAG_OBS - TMS_lag_current; %calculates difference between desired and observed TMS lags
date_end = clock'; %takes note of time at experiment end

returnCLUT=Screen('LoadNormalizedGammaTable',window,gammatable);

KbPressWait; %waits for button press
Screen('CloseAll'); %closes window at end of experiment

%saves workspace as sessionTwo[subject number].mat
filename = 'TMS_strip_'; 
save(['C:\Users\ecenter2\Documents\MATLAB\DATA\' filename, num2str(subj_num)]);