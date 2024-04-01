
export const getAIMessage = async (userQuery) => {

  try {
    // Make a POST request to the Flask API
    const response = await fetch('https://adept-lodge-418903.ue.r.appspot.com/get_response', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: userQuery })
    });

    // Wait for the Flask API to return a response
    const data = await response.text();

    // Construct a message object with the response from the Flask API
    const message = {
      role: "assistant",
      content: data
    };

    return message;

  } catch (error) {
    console.error("Failed to get AI message:", error);
    return {
      role: "assistant",
      content: "Sorry, I couldn't fetch the response."
    };
  }
};
