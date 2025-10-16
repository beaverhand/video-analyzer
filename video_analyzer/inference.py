from client.openai import OpenAIClient
# from client.local import LocalClient
import argparse


def choose_client(client):
    if client == "openai":
        return OpenAIClient()
    # elif client == "local":
    #     return LocalClient(model)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=str, help="Video URL")
    parser.add_argument("--prompt", type=str, help="Prompt")
    parser.add_argument("--video_type", type=str, help="Video Type", default="url")
    parser.add_argument("--client", type=str, help="Client", default="openai")
    args = parser.parse_args()

    client = choose_client(args.client)
    prompt = args.prompt if args.prompt else "Describe the details"
    output = client.invoke(args.video, prompt, args.video_type)
    print(output)

if __name__ == "__main__":
    main()


# Dummy Image Sample Url
# https://yavuzceliker.github.io/sample-images/image-1021.jpg
