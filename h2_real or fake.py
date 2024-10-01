import socket
import re
import random
from time import sleep

# Inverse tempering functions
def untemper(y):
    y = untemper_right(y)
    y = untemper_left(y)
    y = untemper_left2(y)
    y = untemper_right2(y)
    return y

def untemper_right(y):
    y ^= (y >> 18)
    return y

def untemper_left(y):
    y ^= (y << 15) & 0xefc60000
    return y

def untemper_left2(y):
    for _ in range(7):
        y ^= (y << 7) & 0x9d2c5680
    return y

def untemper_right2(y):
    for _ in range(3):
        y ^= (y >> 11)
    return y

def main():
    host = 'cs2107-challs.nusgreyhats.org'
    port = 5051  # Try 5052 or 5053 if needed

    s = socket.socket()
    s.connect((host, port))

    outputs = []
    solved = False
    attempt = 0

    while not solved:
        # Receive data until the prompt
        data = ''
        while True:
            try:
                recv = s.recv(4096).decode()
                if not recv:
                    break
                data += recv
                print(recv, end='')  # Print server response
                if "Guess the output" in data or "flag" in data.lower():
                    break
            except socket.error:
                break

        if "flag" in data.lower():
            print("\nReceived the flag!")
            solved = True
            break

        # Send a dummy guess (e.g., '0')
        s.sendall(b'0\n')

        # Receive the response
        data = ''
        while True:
            try:
                recv = s.recv(4096).decode()
                if not recv:
                    break
                data += recv
                print(recv, end='')  # Print server response
                if "Wrong! It was:" in data or "Correct" in data:
                    break
            except socket.error:
                break

        # Extract the output
        match = re.search(r'Wrong! It was: (\d+)', data)
        if match:
            number = int(match.group(1))
            outputs.append(number)
            attempt += 1
            print(f"\nCollected {len(outputs)} outputs.")

            # Try to predict when we have at least 10 outputs
            if len(outputs) >= 5:
                print("Attempting to predict the next number...")
                # Reconstruct the internal state
                try:
                    mt_state = [untemper(y) for y in outputs[-624:]]
                    # Initialize our own MT19937 with the reconstructed state
                    rng = random.Random()
                    state = (3, tuple(mt_state + [624]), None)
                    rng.setstate(state)
                    # Generate numbers to reach the current position
                    for _ in range(len(outputs), 624):
                        rng.getrandbits(32)
                    # Predict the next number
                    predicted_number = rng.getrandbits(32)
                    print(f"Predicted next number: {predicted_number}")

                    # Receive the next prompt
                    data = ''
                    while True:
                        try:
                            recv = s.recv(4096).decode()
                            if not recv:
                                break
                            data += recv
                            print(recv, end='')  # Print server response
                            if "Guess the output" in data:
                                break
                        except socket.error:
                            break

                    # Send the predicted number
                    s.sendall((str(predicted_number) + '\n').encode())
                    print(f"Sent prediction to server: {predicted_number}")

                    # Receive the response
                    data = ''
                    while True:
                        try:
                            recv = s.recv(4096).decode()
                            if not recv:
                                break
                            data += recv
                            print(recv, end='')  # Print server response
                            if "flag" in data.lower() or "Wrong! It was:" in data:
                                break
                        except socket.error:
                            break

                    if "flag" in data.lower():
                        print("\nReceived the flag!")
                        solved = True
                        break
                    else:
                        # Add the actual output to our outputs
                        match = re.search(r'Wrong! It was: (\d+)', data)
                        if match:
                            number = int(match.group(1))
                            outputs.append(number)
                            attempt += 1
                            print(f"\nCollected {len(outputs)} outputs.")
                        else:
                            print("Failed to extract the output. Continuing...")
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    print("Continuing to collect outputs...")
        else:
            print("Failed to extract the output. Ending session.")
            break

    s.close()

if __name__ == "__main__":
    main()
