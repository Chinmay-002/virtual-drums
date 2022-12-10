import time as t

from VirtualInstrument import *

if __name__ == '__main__':
    # array to store all the virtual instruments
    instruments = []

    # allocate the inuilt webcam as the camera
    camera = cv.VideoCapture(0)

    # capture an image as frame
    _, frame = camera.read()

    # create instances of the virtual instruments defined in VirtualInstrument.py
    hat = VirtualHat()
    instruments.append(hat)
    snare = VirtualSnare()
    instruments.append(snare)

    # format the positions of the instruments on the screen
    l = len(instruments)
    for i in range(l):
        instrument = instruments[i]
        instrument.adjustPosition(i, l, frame)

    # main loop of the program
    while True:

        # capture a new image
        ret, frame = camera.read()
        frame = cv.flip(frame, 1)

        # if the image is not valid, exit while loop
        if not ret:
            break

        # for each instrument detect if there is contact with the preset color object and play sound.
        for instrument in instruments:
            area = np.copy(frame[instrument.top[1]:instrument.btm[1], instrument.top[0]:instrument.btm[0]])
            mask = instrument.detectInRegion(area)
            # Display the object on the output image.
            frame[instrument.top[1]:instrument.btm[1], instrument.top[0]:instrument.btm[0]] = cv.addWeighted(
                instrument.image, 1, area, 1, 0)

        # print the frame post-modification
        cv.imshow('output', frame)

        # exit the program by pressing the 'Q' key on the keyboard
        key = cv.waitKey(1) & 0xFF

        # 'Q' to exit
        if key == ord("q"):
            break

        # checking if contact has been made by any instrument
        contact = False
        for instrument in instruments:
            if instrument.detected:
                contact = True
                break

        # get the current time
        curr_time1 = round(t.time() * 1000)
        curr_time2 = round(t.time() * 1000)

        # if there is contact, wait for 200 ms before a new sound can be produced
        if contact:
            while curr_time2 - curr_time1 < 200:
                ret, frame = camera.read()
                frame = cv.flip(frame, 1)

                if not ret:
                    break

                cv.imshow('output', frame)
                curr_time2 = round(t.time() * 1000)

    # delete the open windows
    camera.release()
    cv.destroyAllWindows()
