function highlightUser(buyerUsername) {
    const coolkids = ["AceLF", "JohnDoe", "JaneSmith"]
    const usernameElement = document.querySelector(`#user-${buyerUsername}`);
    console.log(buyerUsername)
    if (coolkids.includes(buyerUsername)) {
        usernameElement.classList.add("highlight");
    } else {
        usernameElement.classList.add("regular");
    }
}
window.onload = function () {
    const buyers = document.querySelectorAll('.buyer');  // Select all buyers
    buyers.forEach(function(buyer) {
        highlightUser(buyer.innerText);  // Pass each buyer's username to the function
    });

    const sellers = document.querySelectorAll('.seller');  // Select all sellers
    sellers.forEach(function(seller) {
        highlightUser(seller.innerText);  // Pass each seller's username to the function
    });
}