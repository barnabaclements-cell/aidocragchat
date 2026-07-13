import { useState } from "react";
import axios from "axios";

const API_URL = "https://aidocragchat.onrender.com/api";

function Upload() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const uploadFile = async () => {
        if (!file) {
            alert("Select PDF");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await axios.post(
                `${API_URL}/upload/`,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            setMessage(res.data.message);

        } catch (err) {
            console.log("Status:", err.response?.status);
            console.log("Data:", err.response?.data);
            alert(JSON.stringify(err.response?.data));
        }
    };

    return (
        <div className="card">
            <h2>Upload PDF</h2>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <button onClick={uploadFile}>
                Upload
            </button>

            <p>{message}</p>
        </div>
    );
}

export default Upload;