from app.runtime.ai_runtime import AIRuntime


def main():

    runtime = AIRuntime()

    runtime.start()

    print("Solo AI Platform Ready")
    print("Type 'exit' to quit\n")

    while True:

        msg = input("You: ")

        if msg.lower() in ["exit", "quit"]:
            break

        res = runtime.handle_message(msg)

        print("\nAI:", res)


if __name__ == "__main__":
    main()