import axios from 'axios';

const fetchData = async (url, method = 'GET', data = null) => {
  try {
    const response = await axios({
      method: method,
      url: url,
      data: data,
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export default fetchData;
