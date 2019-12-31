$(document).ready(function () {
    function reload() {
        window.location.reload()
    }

    $('#subm').click(function () {
        let refer = $('#ref').val();
        let price = $('#pri').val();
        let quantity = $('#qua').val();

        console.log(refer, price, quantity);
        $.ajax({
            url: '/update-offer-price/',
            dataType: 'json',
            type: 'post',
            data: {'offer_reference': refer, 'price': price, 'quantity': quantity},
            success: function (data) {
                $('#offer_stat').css('display', 'block');
                $('#table').append(
                    `
                            <tr>
                            <td>` + data.status + `</td>
                            <td>` + data.batch_id + `</td>
                            <td>` + data.offer.status + `</td>
                            <td>` + data.offer.product_fnac_id + `</td>
                            <td>` + data.offer.offer_fnac_id + `</td>
                            <td>` + data.offer.offer_seller_id + `</td>
                            <td>` + data.offer.error.text + `</td>
                            </tr>`
                )
            },
            error: function (data) {
                alert('error')
            }
        })
    })
})