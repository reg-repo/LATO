# Examples Used in Prompting Methods

## LATO
### Key Activity Identification
```
Input:
The device at startup should first perform SIM card authentication, verifying the validity and legality of the SIM card. If the SIM card is invalid or unrecognized, prompt the user and block further operations. After authentication succeeds, the device should initiate a multi-factor authentication process (e.g., password, fingerprint, facial recognition), requiring at least two methods to pass according to the user’s configured security level. Each authentication step should include timeout and error-handling mechanisms; if multiple failures occur (e.g., more than three attempts), the device should lock the user account and issue a warning notification. Upon successful authentication, the device should record detailed information about the authentication event—including time, authentication method, and result—for later security review and log analysis. The device should periodically re-verify the user’s identity, especially when abnormal behavior is detected or after extended inactivity, to ensure continuous security.

Output:
[SIM card authentication, prompt user, abort operation, initiate multi-factor authentication, password authentication, fingerprint authentication, facial recognition, record passed methods, timeout and error handling, lock user account, issue warning notification, record authentication event details, periodic re-authentication]

Input:
When a user attempts to enter the system, they must first swipe their card for identity verification. If the card is invalid, the system will deny access and terminate the process; if the card is valid, the system will turn on the lights and start the air conditioning (AC), then execute the subsequent steps in parallel. Based on current temperature conditions, the system will adjust as follows: if it is hot, close the blinds and set the AC to high fan speed; if normal, set the AC to medium fan speed; if cloudy, turn off the AC and open the blinds. While monitoring temperature, the system also activates the environmental sensor for real-time monitoring of smoke. If smoke is detected, the system performs these parallel operations: open the door for rapid evacuation and generate an alarm to alert the user. If no smoke is detected, the system enters sleep mode.

Output:
[user attempts entry, card swipe authentication, deny access, terminate process, turn on lights, start AC, monitor temperature, close blinds, set AC to high speed, set AC to medium speed, turn off AC, open blinds, activate environmental sensor, monitor smoke, open door, allow rapid evacuation, generate alarm, alert user, enter sleep mode]
```
### Layerwise Relation Extraction
```
Input:
The device at startup should first perform SIM card authentication, verifying the validity and legality of the SIM card. If the SIM card is invalid or unrecognized, prompt the user and block further operations. After authentication succeeds, the device should initiate a multi-factor authentication process (e.g., password, fingerprint, facial recognition), requiring at least two methods to pass according to the user’s configured security level. Each authentication step should include timeout and error-handling mechanisms; if multiple failures occur (e.g., more than three attempts), the device should lock the user account and issue a warning notification. Upon successful authentication, the device should record detailed information about the authentication event—including time, authentication method, and result—for later security review and log analysis. The device should periodically re-verify the user’s identity, especially when abnormal behavior is detected or after extended inactivity, to ensure continuous security.

Final Output:
Level 1{
**SIM card authentication** triggers a conditional structure with 2 branches:
  Branch **SIM card invalid or unrecognized**: prompt user -> abort operation -> end
  Branch **SIM card authentication successful**: initiate multi-factor authentication -> [**initiate multi-factor authentication** triggers loop structure] -> authentication success -> record detailed authentication event information -> periodic re-authentication}
Level 2{
**Initiate multi-factor authentication** triggers a loop structure with the loop condition **number of passed authentication methods < 2**:
  [**number of passed authentication methods** triggers parallel structure] -> [**number of authentication failures** triggers conditional structure]}
Level 3{
**Number of passed authentication methods** triggers a parallel structure with 3 branches:
  Branch 1: password verification -> [**password verification** triggers conditional structure]
  Branch 2: fingerprint verification -> [**fingerprint verification** triggers conditional structure]
  Branch 3: facial recognition -> [**facial recognition** triggers conditional structure]
**Number of authentication failures** triggers a conditional structure with 1 branch:
  Branch **authentication failures > 3**: lock user account -> send warning notification -> end}
Level 4{
**Password verification** triggers a conditional structure with 2 branches:
  Branch **authentication success**: record authentication method
  Branch **authentication failure**: timeout and error handling -> authentication failures +1
**Fingerprint verification** triggers a conditional structure with 2 branches:
  Branch **authentication success**: record authentication method
  Branch **authentication failure**: timeout and error handling -> authentication failures +1
**Facial recognition** triggers a conditional structure with 2 branches:
  Branch **authentication success**: record authentication method
  Branch **authentication failure**: timeout and error handling -> authentication failures +1}

Input:
When the user attempts to enter the system, they must first swipe a card to complete identity verification. If the card is invalid, the system will deny access and terminate the process; if the card is valid, the system will first turn on the lights, start the air conditioning (AC), and then execute subsequent steps in parallel. Based on current temperature conditions, the system will make the following adjustments: if the weather is hot, the system will close the blinds and set the AC to high fan speed. If the weather is normal, the system will set the AC to medium fan speed. If the weather is cloudy, the system will turn off the AC and open the blinds. While temperature detection is in progress, the system will activate the environmental sensor for real-time monitoring, primarily to detect the presence of smoke. If smoke is detected, the system will perform the following parallel operations: open the door to allow the user to evacuate quickly; generate an alarm to alert the user. If no smoke is detected, the system will enter sleep mode.

Final Output:
Level 1{
**Card verification** triggers a conditional structure with 2 branches:
  Branch **card invalid**: deny access -> terminate process -> end
  Branch **card valid**: turn on lights -> start AC -> [**start AC** triggers parallel structure]}
Level 2{
**Start AC** triggers a parallel structure with 2 branches:
  Branch 1: temperature monitoring -> [**temperature monitoring** triggers conditional structure]
  Branch 2: activate environmental sensor -> smoke monitoring -> [**smoke monitoring** triggers conditional structure]}
Level 3{
**Temperature monitoring** triggers a conditional structure with 3 branches:
  Branch **hot weather**: close blinds -> set AC to high fan speed
  Branch **normal weather**: set AC to medium fan speed
  Branch **cloudy weather**: turn off AC -> open blinds
**Smoke monitoring** triggers a conditional structure with 2 branches:
  Branch **smoke detected**: [**smoke detected** triggers parallel structure]
  Branch **no smoke detected**: enter sleep mode}
Level 4{
**Smoke detected** triggers a parallel structure with 2 branches:
  Branch 1: open door -> allow user quick evacuation
  Branch 2: generate alarm -> alert user}
```

### Behaviroal Model Constructor
```
Input:
The device, upon startup, should first perform SIM card authentication, verifying the validity and legitimacy of the SIM card. If the SIM card is invalid or unrecognized, it should prompt the user and abort any further operations. Once authentication succeeds, the device should initiate a multi-factor authentication process (e.g., password, fingerprint, facial recognition), requiring at least two authentication methods to pass based on the user’s configured security level. Each authentication step should include timeout and error-handling mechanisms; if authentication fails multiple times (e.g., more than 3 times), the device should lock the user account and send a warning notification. After successful authentication, the device should log detailed information about the authentication event, including the time, methods used, and result, for subsequent security review and log analysis. The device should periodically re-verify the user’s identity, especially when abnormal behavior is detected or after long periods of inactivity, to ensure continuous security.

#Activity Identification
SIM card authentication, prompt user, abort operation, initiate multi-factor authentication, password recognition, fingerprint recognition, facial recognition, record successful authentication method, timeout and error handling, lock user account, send warning notification, authentication successful, log authentication event details, periodic re-authentication

#Relation Decomposition
Level 1{
**SIM card authentication** triggers a conditional structure, with 2 branches:
  Branch **SIM card invalid or unrecognized**: prompt user -> abort operation -> end
  Branch **SIM card authenticated successfully**: initiate multi-factor authentication -> [**initiate multi-factor authentication** triggers a loop structure] -> authentication successful -> log authentication event details -> periodic re-authentication}
Level 2{
**Initiate multi-factor authentication** triggers a loop structure, looping while **number of passed authentication methods < 2**:
  [**number of passed authentication methods** triggers a parallel structure] -> [**authentication failure count** triggers a conditional structure]}
Level 3{
**Number of passed authentication methods** triggers a parallel structure, with 3 branches:
  Branch 1: password recognition -> [**password recognition** triggers a conditional structure]
  Branch 2: fingerprint recognition -> [**fingerprint recognition** triggers a conditional structure]
  Branch 3: facial recognition -> [**facial recognition** triggers a conditional structure]
**Authentication failure count** triggers a conditional structure, with 1 branch:
  Branch **authentication failure count > 3**: lock user account -> send warning notification -> end}
Level 4{
**Password recognition** triggers a conditional structure, with 2 branches:
  Branch **authentication successful**: record successful authentication method
  Branch **authentication failed**: timeout and error handling -> increment authentication failure count
**Fingerprint recognition** triggers a conditional structure, with 2 branches:
  Branch **authentication successful**: record successful authentication method
  Branch **authentication failed**: timeout and error handling -> increment authentication failure count
**Facial recognition** triggers a conditional structure, with 2 branches:
  Branch **authentication successful**: record successful authentication method
  Branch **authentication failed**: timeout and error handling -> increment authentication failure count}

Please understand the decomposition above and write a Information Integration, ensuring necessary descriptive details remain consistent with the input text.

Output:
SIM card authentication
if SIM card invalid/unrecognized
    prompt user
    abort operation
else
    initiate multi-factor authentication
    while number of passed authentication methods < 2
        fork
            password recognition
            if authentication successful
                record successful authentication method
            else
                timeout and error handling
                authentication failure count + 1
        fork
            fingerprint recognition
            if authentication successful
                record successful authentication method
            else
                timeout and error handling
                authentication failure count + 1
        fork
            facial recognition
            if authentication successful
                record successful authentication method
            else
                timeout and error handling
                authentication failure count + 1
        if authentication failure count > 3
            lock user account
            send warning notification
            end
    authentication successful
    log authentication event details
    periodic re-authentication

Input:
When a user attempts to access the system, they must first swipe their card to complete identity verification. If the card is invalid, the system will deny access and terminate the process; if the card is valid, the system will first turn on the lights, start the air conditioning (AC), and then execute subsequent steps in parallel. Depending on the current temperature conditions, the system will make the following adjustments: if the weather is hot, the system will close the blinds and set the AC to high fan speed. If the weather is normal, the system will set the AC to medium fan speed. If the weather is cloudy, the system will turn off the AC and open the blinds. Simultaneously with temperature detection, the system will activate environmental sensors for real-time monitoring, primarily to detect the presence of smoke. If smoke is detected, the system will perform the following parallel operations: open the door to allow quick evacuation; generate an alarm to alert the user. If no smoke is detected, the system will enter sleep mode.

#Activity Identification
user enters system, card swipe authentication, deny access, terminate process, turn on lights, start air conditioning, temperature monitoring, close blinds, set AC to high fan speed, set AC to medium fan speed, turn off AC, open blinds, activate environmental sensors, smoke monitoring, open door, allow quick evacuation, generate alarm, alert user, enter sleep mode

#Relation Decomposition
Level 1{
**Card swipe authentication** triggers a conditional structure, with 2 branches:
  Branch **card invalid**: deny access -> terminate process -> end
  Branch **card valid**: turn on lights -> start air conditioning -> [**start air conditioning** triggers a parallel structure]}
Level 2{
**Start air conditioning** triggers a parallel structure, with 2 branches:
  Branch 1: temperature monitoring -> [**temperature monitoring** triggers a conditional structure]
  Branch 2: activate environmental sensors -> smoke monitoring -> [**smoke monitoring** triggers a conditional structure]}
Level 3{
**Temperature monitoring** triggers a conditional structure, with 3 branches:
  Branch **weather is hot**: close blinds -> set AC to high fan speed
  Branch **weather is normal**: set AC to medium fan speed
  Branch **weather is cloudy**: turn off AC -> open blinds
**Smoke monitoring** triggers a conditional structure, with 2 branches:
  Branch **smoke detected**: [**smoke detected** triggers a parallel structure]
  Branch **no smoke detected**: enter sleep mode}
Level 4{
**Smoke detected** triggers a parallel structure, with 2 branches:
  Branch 1: open door -> allow quick evacuation
  Branch 2: generate alarm -> alert user}

Please understand the decomposition above and write a Information Integration, ensuring necessary descriptive details remain consistent with the input text.

Output:
user enters system
card swipe authentication
if card invalid
  deny access
  terminate process
else
  turn on lights
  start air conditioning
  fork
    temperature monitoring
    if weather is hot
      close blinds
      set AC to high fan speed
    elif weather is normal
      set AC to medium fan speed
    else
      turn off AC
      open blinds
  fork
    activate environmental sensors
    smoke monitoring
    if smoke detected
      fork
        open door
        allow quick evacuation
      fork
        generate alarm
        alert user
    else
      enter sleep mode
```
```
Input:
On device startup, the device should first perform SIM card authentication to verify the SIM card’s validity and legitimacy. If the SIM card is invalid or unrecognized, prompt the user and block further operations. After successful authentication, the device should initiate a multi-factor authentication flow (e.g., password, fingerprint, facial recognition), requiring at least two authentication methods to pass based on the user’s configured security level. Each authentication step should include timeout and error-handling mechanisms. If multiple authentication failures occur (e.g., more than 3 times), the device should lock the user’s account and issue a warning notification. Upon successful authentication, the device should log detailed information about the authentication event, including timestamp, authentication methods, and results for subsequent security review and log analysis. The device should periodically re-verify the user’s identity, especially when detecting anomalous behavior or prolonged inactivity, to ensure continuous security.

#Information Integration
SIM card authentication
if SIM card invalid/unrecognized
    prompt user
    abort operation
else
    initiate multi-factor authentication
    while number of passed methods < 2
        fork
            password verification
            if success
                record authentication method
            else
                timeout and error handling
                failure count +1
        fork
            fingerprint scan
            if success
                record authentication method
            else
                timeout and error handling
                failure count +1
        fork
            facial recognition
            if success
                record authentication method
            else
                timeout and error handling
                failure count +1
        if failure count > 3
            lock user account
            issue warning notification
            end
    authentication success
    log authentication event details
    periodic re-verification

Output:
start
  :Perform SIM card authentication;
  if (Is SIM card valid?) then (yes)
     :Initiate multi-factor authentication;
     :Select authentication methods;
     repeat
       fork
         :Enter password;
         if (Is password correct?) then (yes)
           :Record authentication details;
         else (no)
           :Timeout and error handling;
         endif
       fork again
         :Scan fingerprint;
         if (Is fingerprint matched?) then (yes)
           :Record authentication details;
         else (no)
           :Timeout and error handling;
         endif
       fork again
         :Perform facial recognition;
         if (Is facial recognition successful?) then (yes)
           :Record authentication details;
         else (no)
           :Timeout and error handling;
         endif
       end fork
       if (Failure count > 3) then (yes)
         :Lock account;
         :Send alert notification;
         stop
       else (no)
         :Continue authentication;
       endif
     repeat while (At least two authentication methods successful)
     :Authentication successful;
     :Log authentication event;
  else (no)
     :Notify invalid SIM card;
     stop
  endif
  :Periodically re-verify;
stop


Input:
When a user attempts to enter the system, they must first swipe a card to complete identity verification. If the card is invalid, the system will deny access and terminate the flow; if the card is valid, the system will first turn on the lights, start the air conditioning (AC), and then execute subsequent steps in parallel. Based on current temperature conditions, the system will make the following adjustments: if it is hot, the system will close the blinds and set the AC to high fan speed; if normal, it will set the AC to medium fan speed; if cloudy, it will turn off the AC and open the blinds. Simultaneously with temperature detection, the system will activate environmental sensors for real-time monitoring, primarily detecting the presence of smoke. If smoke is detected, the system will perform the following parallel actions: open the door to allow the user to evacuate quickly; generate an alarm to alert the user. If no smoke is detected, the system will enter sleep mode.

#Information Integration
user entrance attempt
swipe card verification
if card invalid
  deny access
  terminate flow
else
  turn on lights
  start AC
  fork
    temperature monitoring
    if hot weather
      close blinds
      set AC to high speed
    elif normal weather
      set AC to medium speed
    else
      turn off AC
      open blinds
  fork
    activate environmental sensors
    smoke detection
    if smoke detected
      fork
        open door
        allow quick evacuation
      fork
        generate alarm
        alert user
    else
      enter sleep mode

Output:
start
:Swipe card for entrance;
:verify user;
if (valid?) then (yes)
    :ON Lights;
    :Activate Sensor;
    :Set AC;
    fork
    :Check Temperature;
    switch()
    case (Hot)
        :Close Blinds and Set Ac to High;
    case (normal)
        :Set AC to Medium;
    case (Cloudy)
        :OFF AC and open Blinds;
    endswitch
    fork again
        :Activate Sensor;
        :Detect Smoke;
    if (detected?) then (yes)
        fork
           :Open Door;
        fork again
           :Generate Alarm;
        end fork
    else (no)
    endif
    :exit;
    :Activate Sleep mode;
    end fork
    stop
else (no)
    :Rejected;
    stop
```
## Zero-shot
```
Input:
{Input}

Please generate PlantUML code for the activity diagram according to the above requirements. Output the results directly without explanation

Output:
```
## Few-shot
```
Input:
When the device powers on, it should first perform SIM card authentication to verify the SIM card’s validity and legitimacy. If the SIM card is invalid or unrecognized, prompt the user and block further operations. After authentication succeeds, the device should initiate a multi-factor authentication flow (such as password, fingerprint, facial recognition), requiring at least two authentication methods to pass according to the user’s configured security level. Each authentication step should include timeout and error-handling mechanisms; if multiple authentication failures occur (e.g., more than 3 times), the device should lock the user’s account and issue a warning notification. Upon successful authentication, the device should log detailed information about the authentication event—including timestamp, authentication method, and result—for subsequent security review and log analysis. The device should periodically re-verify the user’s identity, especially when detecting anomalous behavior or prolonged inactivity, to ensure continuous security.

Please generate the PlantUML code for the activity diagram based on the above requirements. Output the result directly without explanation.

Output:
start
  :Perform SIM card authentication;
  if (SIM card valid?) then (yes)
     :Initiate multi-factor authentication;
     :Select authentication methods;
	 repeat
	   fork
	     :Enter password;
	     if (Password correct?) then (yes)
	       :Log authentication details;
	     else (no)
	       :Handle timeout and errors;
	     endif
	   fork again
	     :Scan fingerprint;
	     if (Fingerprint match?) then (yes)
	       :Log authentication details;
	     else (no)
	       :Handle timeout and errors;
	     endif
	   fork again
	     :Facial recognition;
	     if (Face recognition passed?) then (yes)
	       :Log authentication details;
	     else (no)
	       :Handle timeout and errors;
	     endif
	   end fork
	   if (Failure count > 3) then (yes)
	     :Lock account;
	     :Issue warning notification;
	     stop
	   else (no)
	     :Continue authentication;
	   endif
	 repeat while (At least two methods succeeded)
	 :Authentication successful;
	 :Log authentication event;
	else (no)
	 :Prompt invalid SIM card;
	 stop
	endif
	:Periodically re-verify;
	stop


Input:
When a user attempts to enter the system, they must first swipe their access card to complete identity verification. If the card is invalid, the system will deny access and terminate the flow; if the card is valid, the system will first turn on the lights, activate the air conditioner (AC), then execute the following steps in parallel. Based on the current temperature conditions, the system will make these adjustments: if it’s hot, the system will close the blinds and set the AC to high fan speed; if it’s normal, the system will set the AC to medium fan speed; if it’s cloudy, the system will turn off the AC and open the blinds. While detecting temperature, the system will also activate environmental sensors for real-time monitoring, primarily to detect smoke. If smoke is detected, the system will perform the following parallel actions: open the door to allow quick evacuation and generate an alarm to alert the user. If no smoke is detected, the system will enter sleep mode.

Please generate the PlantUML code for the activity diagram based on the above requirements. Output the result directly without explanation.

Output:
start
:Swipe card for entrance;
:verify user;
if (valid?) then (yes)
    :ON Lights;
    :Activate Sensor;
    :Set AC;
    fork
    :Check Temperature;
    switch()
    case (Hot)
        :Close Blinds and Set AC to High;
    case (normal)
        :Set AC to Medium;
    case (Cloudy)
        :OFF AC and open Blinds;
    endswitch
    fork again
        :Activate Sensor;
        :Detect Smoke;
    if (detected?) then (yes)
        fork
           :Open Door;
        fork again
           :Generate Alarm;
        end fork
    else (no)
    endif
    :exit;
    :Activate Sleep mode;
    end fork
    stop
else (no)
    :Rejected;
    stop
```
## Chain-of-Thought
```
Input:
The device should first perform SIM card authentication at startup, verifying the validity and legitimacy of the SIM card. If the SIM card is invalid or unrecognized, prompt the user and prevent further operation. After authentication passes, the device should initiate a multi-factor authentication process (e.g., password, fingerprint, facial recognition), requiring at least two authentication methods to pass based on the user-defined security level. Each authentication step should include timeout and error handling mechanisms; if multiple authentication failures occur (e.g., more than 3 times), the device should lock the user account and issue a warning notification. Upon successful authentication, the device should record detailed information of the authentication event, including time, method, and result, for subsequent security review and log analysis. The device should periodically re-verify the user's identity, especially when detecting abnormal behavior or prolonged inactivity, to ensure continuous security.

Please generate PlantUML code for the activity diagram according to the above requirements.

Steps:
1. Identify the main activities in the process flow:
   - SIM card authentication
   - Multi-factor authentication selection
   - Password authentication
   - Fingerprint scanning
   - Facial recognition
   - Authentication logging
   - Failure handling
   - Account locking
   - Periodic re-verification
2. Determine the logical sequence and dependencies between activities:
   - SIM card validity check precedes multi-factor authentication
   - Multi-factor authentication branches into three parallel methods
   - Authentication methods have independent success/failure paths
   - Failure count tracking affects retry logic
   - Success requires at least two methods to pass
   - Periodic re-verification follows successful authentication
3. Identify decision points and conditional flows:
   - SIM card validity check (valid/invalid)
   - Authentication method selection (password/fingerprint/face)
   - Authentication result for each method (success/failure)
   - Failure count threshold (≤3/>3)
   - Multi-factor success criteria (≥2 methods passed)
4. Define loops and repetitive processes:
   - Retry authentication up to 3 times on failure
   - Periodic re-verification after successful authentication
5. Determine swimlanes or partitioning (if applicable):
   - User actions vs. System actions
   - Authentication methods grouped logically
6. Generate PlantUML activity diagram code with clear annotations:
   - Include start/end nodes
   - Use proper decision diamond notation
   - Represent parallel flows with fork/join
   - Add notes for important conditions
   - Ensure flow arrows clearly show sequence
   - Use color or styling to differentiate critical paths

Output:
start
  :Perform SIM card authentication;
  if (SIM card valid?) then (yes)
     :Start multi-factor authentication;
     :Choose authentication method;
     repeat
       fork
         :Enter password;
         if (password correct?) then (yes)
           :Log authentication details;
         else (no)
           :Timeout and error handling;
         endif
       fork again
         :Scan fingerprint;
         if (fingerprint match?) then (yes)
           :Log authentication details;
         else (no)
           :Timeout and error handling;
         endif
       fork again
         :Facial recognition;
         if (facial recognition passed?) then (yes)
           :Log authentication details;
         else (no)
           :Timeout and error handling;
         endif
       end fork
       if (failure count > 3) then (yes)
         :Lock account;
         :Issue warning notification;
         stop
       else (no)
         :Continue authentication;
       endif
     repeat while (At least two authentication methods succeeded)
     :Authentication successful;
     :Log authentication event;
  else (no)
     :Prompt “Invalid SIM card”;
     stop
  endif
  :Periodic re-verification;
stop

Input:
When the user attempts to enter the system, they must swipe a card to complete identity verification. If the card is invalid, the system will deny access and terminate the process; if the card is valid, the system will first turn on lights and start the air conditioner (AC), then execute subsequent steps in parallel. Based on the current temperature conditions, the system will make the following adjustments: if the weather is hot, the system will close blinds and set the AC to high fan speed. If the weather is normal, the system will set the AC to medium fan speed. If the weather is cloudy, the system will turn off the AC and open the blinds. While detecting temperature, the system will activate environmental sensors for real-time monitoring, mainly for smoke detection. If smoke is detected, the system will perform the following parallel operations: open the door to allow rapid user evacuation; generate an alarm to alert the user. If no smoke is detected, the system will enter sleep mode.

Please generate PlantUML code for the activity diagram according to the above requirements.

Steps:
1. Analyze core activities:
   - User identity verification
   - Environmental device control (lights, AC, blinds)
   - Temperature-based adjustments
   - Smoke detection & emergency response
   - System exit & sleep mode activation
2. Determine sequence & dependencies:
   - Verification → Environmental control → Concurrent safety checks → Exit
   - Environmental control depends on verification success
   - Safety detection runs in parallel with device control
3. Identify decision points:
   - Verification pass/fail
   - Temperature threshold check
   - Smoke detection trigger
4. Mark parallel flows:
   - Use fork/join for concurrent environmental control and safety detection
5. Define termination conditions:
   - Verification failure stops process
   - Normal completion activates sleep mode
   - Smoke detection triggers emergency exit
6. Generate PlantUML structure:
   - Use standard symbols (rounded rectangles, diamonds, arrows)
   - Clearly show decision points and conditions
   - Group related activities
   - Ensure flow matches requirement logic

Output:
start
:Swipe card for entrance;
:verify user;
if (valid?) then (yes)
    :ON Lights;
    :Activate Sensor;
    :Set AC;
    fork
    :Check Temperature;
    switch()
    case (Hot)
        :Close Blinds and Set AC to High;
    case (normal)
        :Set AC to Medium;
    case (Cloudy)
        :OFF AC and open Blinds;
    endswitch
    fork again
        :Activate Sensor;
        :Detect Smoke;
    if (detected?) then (yes)
        fork
           :Open Door;
        fork again
           :Generate Alarm;
        end fork
    else (no)
    endif
    :exit;
    :Activate Sleep mode;
    end fork
    stop
else (no)
    :Rejected;
    stop
```
## Output Instance
### Example Input
After the system starts up, the process begins by checking the gear position. If the gear is in D or N, the D_S gear mileage parameter is set to 1, and the sequence ends. If the gear is in S, the D_S gear mileage parameter is calculated as S gear nominal mileage divided by D gear nominal mileage, then the process concludes. Additionally, if the vehicle status is 30, switch to driving mode. Next, if the gear is in D or E, set the D_S gear mileage parameter to S gear nominal mileage divided by D gear nominal mileage, and end. Finally, if the gear is in N or R, observe using the D_S gear mileage parameter and terminate the process.
### Generated Code
```
@startuml
start
:Check gear position;
if (Gear in D or N?) then (yes)
  :Set D_S gear mileage parameter to 1;
  stop
elseif (Gear in S?) then (yes)
  :Calculate D_S gear mileage parameter\n(S gear nominal mileage / D gear nominal mileage);
  stop
elseif (Vehicle status is 30?) then (yes)
  :Switch to driving mode;
  if (Gear in D or E?) then (yes)
    :Set D_S gear mileage parameter\n(S gear nominal mileage / D gear nominal mileage);
    stop
  else (no)
  endif
elseif (Gear in N or R?) then (yes)
  :Observe D_S gear mileage parameter;
  stop
else (no)
  stop
endif
stop
@enduml
```
### Rendring Diagram
<div align="center">
  <img src="Figures/p_example.png" alt="Example" width="100%"/>
  <p><em>Example Output Instance</em></p>
</div>
