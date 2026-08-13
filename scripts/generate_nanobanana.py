import os
import sys

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai is not installed.")
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_nanobanana.py <prompt> <output_path>")
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = sys.argv[2]
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    print(f"Generating image with model: gemini-3.1-flash-lite-image using generate_content")
    print(f"Prompt: {prompt}")

    try:
        # gemini-3.1-flash-lite-image は generate_content メソッドで画像を生成する
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-image',
            contents=prompt,
        )
        
        # レスポンスから画像のバイトデータを抽出
        saved = False
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    with open(output_path, 'wb') as f:
                        f.write(part.inline_data.data)
                    print(f"Success! Image saved to {output_path}")
                    saved = True
                    break
                elif hasattr(part, 'text') and part.text:
                    print(f"Text output received: {part.text}")
                    
        if not saved:
            print("No image data found in response parts.")
            
    except Exception as e:
        print(f"Error generating image: {e}")

if __name__ == "__main__":
    main()
