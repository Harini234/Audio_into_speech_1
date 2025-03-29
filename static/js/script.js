document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("OrderTaken").addEventListener("change", toggleUpload);
    document.getElementById("orderForm").addEventListener("submit", validateOrder);
    document.getElementById("recordAudioBtn").addEventListener("click", recordLiveAudio);
    // document.getElementById("TransactionType").addEventListener("oninput", validateOrder);
});



function toggleUpload() {
    const orderTaken = document.getElementById("OrderTaken").value;
    const uploadAudio = document.getElementById("uploadAudio");
    const recordButtons = document.getElementById("recordButtons");
    
    if (orderTaken.includes("Received")) {
        uploadAudio.style.display = "block";
        recordButtons.style.display = "none";
    } else {
        uploadAudio.style.display = "none";
        recordButtons.style.display = "block";
    }
}

function startRecording() {
    alert("Recording started.");
    recordLiveAudio()
}

function stopRecording() {
    alert("Recording stopped.");

}

async function uploadAudio() {
    const fileInput = document.getElementById("audioFile");
    
    if (!fileInput.files.length) {
        alert("Please select an audio file");
        return;
    }
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    try {
        const response = await fetch("http://127.0.0.1:8000/convert-audio-to-text/", {
            method: "POST",
            body: formData
        });
        const result = await response.json();
        const transcribed_text = document.getElementById("Transcribed_text");
        transcribed_text.value = result.converted_text;
        if (!response.ok) {
            throw new Error("Failed to upload audio");
        }
        
    } catch (error) {
        alert("Error uploading file: " + error.message);
        console.error("Upload error:", error);
    }
}

async function recordLiveAudio() {
    try {
        const response = await fetch("http://127.0.0.1:8000/record-live-audio/?duration=60&model_size=base", {
            method: "POST",
        });
        
        if (!response.ok) {
            throw new Error("Failed to record audio");
        }
        
        const result = await response.json();
        document.getElementById("Transcribed_text").value = result.converted_text || "Recording Failed";
    } catch (error) {
        alert("Error recording audio: " + error.message);
        console.error("Recording error:", error);
    }
}

function checkFormCompletion() {
    var transactionType = document.getElementById('TransactionType').value;
    var quantity = document.getElementById('Quantity').value.trim();
    var symbol = document.getElementById('Symbol').value.trim();
    // alert("message")
    var continueButton = document.getElementById('Continue');

    if (transactionType !== "" && quantity !== "" && symbol !== "") {
        continueButton.disabled = false;
    } else {
        continueButton.disabled = true;
    }
    document.getElementById("TransactionType").addEventListener("oninput", validateOrder);
}


async function validateOrder(event) {
    event.preventDefault();
    
    const form = document.getElementById("orderForm");
    const formData = {
        order_type: document.getElementById("TransactionType").value,
        quantity: document.getElementById("Quantity").value,
        symbol: document.getElementById("Symbol").value,
        Transcribed_text: document.getElementById("Transcribed_text").value
    };
    
    form.querySelectorAll("input, select, textarea").forEach((input) => {
        if (input.id) {
            formData[input.id] = input.value;
        }
    });

    const transcribeElement = document.getElementById("Transcribed_text");
    const transcribed_text = transcribeElement ? transcribeElement.value: "";
    
    try {
        const response = await fetch("http://127.0.0.1:8092/validate_input/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });
        
        const result = await response.json();
        let mismatchdata = result.mismatch_data;
        
        if (mismatchdata && mismatchdata.length > 0) {
            let alertMessage = "Mismatch Found: \n";
            mismatchdata.forEach((item, index) => {
                alertMessage += `${index + 1}.${item.status}: ${item.Mismatch_data}\n`;
            });
            alert(alertMessage);
        } else {
            alert("All data matching");
        }
    } catch (error) {
        alert("Error Validating Order Details: " + error.message);
        console.error("Validation error:", error);
    }
}