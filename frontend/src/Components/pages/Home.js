import React, { Component } from 'react'

class Home extends Component {
    constructor() {
        super()
        this.state = {

            response: {}
        }
        this.handleChange = this.handleChange.bind(this);
        this.submitForm = this.submitForm.bind(this)
    }
    handleChange(event) {
        this.setState({ value: event.target.value });
    }
    submitForm(e) {
        e.preventDefault();
        fetch('http://127.0.0.1:5000/api/predict/dryer', {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: 'follow', // manual, *follow, error
            referrer: 'no-referrer', // no-referrer, *client
            body: JSON.stringify({
                "specifications": ["AS/NZS 2442.2:2000/Amdt 2:2007 (Legacy)",
                    "ASKO", 8, true, "Timer", "Slovenia", 890, 650, 200, "Heat and dry", 230, "Vented", 650, "10/26/2020"]
            }),
        })
            .then(response => response.json())
            .then(res => {
                console.log(res);
                this.setState({ response: res })
            })
    }
    render() {
        return (
            <div className='landing'>
                <form className='dark-overlay text-dark'>
                    <label className='form-group'>Appliance Standard
                    <input
                            type='text'
                            placeholder='Appliance Standard'
                            value={this.state.applianceStandard}
                            onChange={this.handleChange}

                        /></label>
                    <br />
                    <button
                        type='submit'
                        className='form-group btn btn-dark'
                        onClick={this.submitForm}
                    >
                        Submit
          </button>
                </form>
                <label className="display-4">{this.state.response.info}</label>
            </div>
        )
    }
}

export default Home
