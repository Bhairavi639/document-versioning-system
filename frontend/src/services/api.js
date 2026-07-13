import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const compareDocuments = async (file1, file2) => {
    const formData = new FormData();

    formData.append("file1", file1);
    formData.append("file2", file2);

    const response = await axios.post(
        `${API_BASE_URL}/compare`,
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};