response = {
  "id": "chatcmpl-7URR1AcDTuid60jRD9G3tU9CNcNtj",
  "object": "chat.completion",
  "created": 1687489655,
  "model": "gpt-3.5-turbo-0301",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "My dearest grandson,\n\nI am so proud of you for embarking on this new journey of starting your first job. Congratulations on this achievement! It shows your hard work and dedication in pursuing your dreams.\n\nAs you begin this new chapter, I want to give you some advice that I have learned through my own experiences. First and foremost, always remember the importance of family. No matter how busy you get with your job, make sure to prioritize spending time with your loved ones. They offer support, love, and a reminder of what truly matters in life.\n\nSecondly, always stay focused. Dedication and hard work will lead you to success. Do not let distractions deter you from your goals. You are a bright young man and I know that with your focus and determination, you can accomplish anything you set your mind to.\n\nFurthermore, be always willing to lend a helping hand. Your kindness and friendly personality are traits that are highly valued in any workplace. Be respectful to your colleagues and offer help whenever you can. This will not only make your work environment a positive one but also foster strong relationships with your colleagues.\n\nFinally, do not be afraid to let your creativity shine. Your creativity is a gift that can set you apart in any job. Find ways to be innovative, solve problems differently, and add value to your company.\n\nI believe that with these values and traits, you will be a great asset to any job you take on. I am always here to offer you support and guidance.\n\nCongratulations once again. I love you and wish you all the best in your future endeavors.\n\nSincerely,\n\nGrandfather."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 76,
    "completion_tokens": 324,
    "total_tokens": 400
  }
}

print(response["choices"][0]["message"]["content"])
