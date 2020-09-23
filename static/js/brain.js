var countDownTo = new Date("Oct 10, 2020 05:00:00").getTime(); // Start of the contest date

var x = setInterval(function() { // Display the time passed since last update
        var now = new Date;
        var timestamp = now.getUTCFullYear().toString() + "-" + (now.getUTCMonth() + 1).toString().padStart(2, '0') + "-" + now.getUTCDate().toString().padStart(2, '0') + " " + now.getUTCHours().toString().padStart(2, '0') + ":" + now.getUTCMinutes().toString().padStart(2, '0') + ":" + now.getUTCSeconds().toString().padStart(2, '0')
        var utc_timestamp = new Date(timestamp).getTime();

        if (countDownTo >= utc_timestamp) {
            var difference = countDownTo - utc_timestamp;
            var days = Math.floor(difference / (1000 * 60 * 60 * 24));
            var hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((difference % (1000 * 60)) / 1000);


            document.getElementById("countDown").innerHTML = days + " d  " + hours + " hr  " + minutes + " m  " + seconds + " s";
        }

    },
    1000);