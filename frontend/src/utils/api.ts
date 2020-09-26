import {NewQueryInterface, QueryInterface} from "../models/interfaces";

const API_URL = (
    window
    && "location" in window
    && "protocol" in window.location
    && "host" in window.location
    && false
) ? window.location.protocol + "//" + window.location.host + "/api" : 'http://localhost:8000/api';

export const apiGetQueries = async () =>
    await fetch(`${API_URL}/queries/`).then(res => {
        if (res.status !== 200) return []
        try {
            return res.json();
        } catch (err) {
            return []
        }
    })

export const apiPostQuery = async (data: NewQueryInterface, force: string | undefined = undefined) =>
    await fetch(`${API_URL}/queries/${force ? `?force=${force}` : ''}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then((res) => {
        if (res.status !== 200) return null
        try {
            return res.json();
        } catch (err) {
            return null
        }
    })

// /**
//  * Api to create pizza.
//  * return null if response status is not 200
//  *
//  * @param data CreatePizzaInterface
//  */
// export const apiCreatePizza = async (data: CreatePizzaInterface) =>
//     await fetch(PIZZAS_URL, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//     }).then((res) => {
//         if (res.status !== 200) return null
//         try {
//             return res.json();
//         } catch (err) {
//             return null
//         }
//     })
//
// /**
//  * Api to update pizzas.
//  * return null if response status is not 200
//  *
//  * @param data CreatePizzaInterface
//  */
// export const apiUpdatePizza = async (data: PizzaInterface) =>
//     await fetch(PIZZAS_URL, {
//         method: 'PUT',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//     }).then(res => {
//         if (res.status !== 200) return null
//         try {
//             return res.json();
//         } catch (err) {
//             return null
//         }
//     })
