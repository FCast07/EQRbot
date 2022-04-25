# EQRbot
The presented code provides a simple implementation of the chatbot introduced in our paper "Providing Explanations Via EQR Argument Scheme", submitted to COMMA 2022. 
The chatbot is in charge of conveying explanations to a patient via an Explanation-Question-Response (EQR) dialogue. These explanations are the product of an argumentation-based reasoning engine computation (which resorts to a modification of the algorithm developed in [1]), and templates of natural language texts.

- Python3 and [DLV](https://www.dlvsystem.it/dlvsite/) (once DLV is downloaded, change the executable file name into 'dlv' and move it into the root folder) should be installed on the system in order to run the code.

- The file REQUIREMENTS.txt lists all the Python packages that should be installed.   

- In the root directory, the following code should be invoked on the terminal: `python EQRbot.py frida/kb.dl frida/attacks.dl frida/frida.dl` (the code had been tested on Windows and Linux).

- After running the code, the terminal will display the explanations instantiated by the acceptable arguments, and then the chatbot will begin its dialogue with the user (who will be conversating as Frida, a fictitious patient). Try asking questions such as "Are there any alternative treatments?", "Why rely on the proposed field of expertise?" or "Why follow the recommendation of the chosen expert?" (after having specified, when prompted, the appropriate context).


[1] _Kökciyan, Nadin, et al. "An argumentation-based approach to generate domain-specific explanations." Multi-Agent Systems and Agreement Technologies. Springer, Cham, 2020. 319-337._  
