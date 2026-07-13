import React, { useState } from "react";
import { compareDocuments } from "../services/api";

function Compare() {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);

    const [diffData, setDiffData] = useState([]);

    const [loading, setLoading] = useState(false);

    const handleCompare = async () => {
        if (!file1 || !file2) {
            alert("Please select both files.");
            return;
        }

        try {
            setLoading(true);

            const result = await compareDocuments(file1, file2);

            setDiffData(result.diff);

        } catch (error) {
    console.error("Comparison Error:", error);

    if (error.response) {
        console.log("Backend Response:", error.response.data);
        console.log("Status:", error.response.status);

        alert(
            `Backend Error (${error.response.status}): ` +
            JSON.stringify(error.response.data)
        );
    } else {
        alert(error.message);
    }
} finally {
            setLoading(false);
        }
    };

    return (
        <div>

            <h2>Document Version Comparison</h2>

            <div>
                <p>Version 1</p>

                <input
                    type="file"
                    accept=".xlsx"
                    onChange={(e) => setFile1(e.target.files[0])}
                />
            </div>

            <br />

            <div>
                <p>Version 2</p>

                <input
                    type="file"
                    accept=".xlsx"
                    onChange={(e) => setFile2(e.target.files[0])}
                />
            </div>

            <br />

            <button onClick={handleCompare}>
                Compare
            </button>

            <br />
            <br />

            {loading && <p>Comparing documents...</p>}

            {diffData.length > 0 && (
                <table border="1" cellPadding="10">

                    <thead>
                        <tr>
                            <th>S.No</th>
                            <th>Row</th>
                            <th>Column</th>
                            <th>Type</th>
                            <th>Old Value</th>
                            <th>New Value</th>
                        </tr>
                    </thead>

                    <tbody>
                        {diffData.map((change, index) => (
                            <tr key={index}>
                                <td>{change.row}</td>
                                <td>{change.column}</td>

                                <td>{change.type}</td>

                                <td>
                                    {change.old || "-"}
                                </td>

                                <td>
                                    {change.new || "-"}
                                </td>
                            </tr>
                        ))}
                    </tbody>

                </table>
            )}

        </div>
    );
}

export default Compare;