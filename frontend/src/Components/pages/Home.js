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
        fetch('/api/predict/dryer', {
            method: 'POST', 
            mode: 'cors', 
            cache: 'no-cache', 
            credentials: 'same-origin', 
            headers: {
                'Content-Type': 'application/json',
            },
            redirect: 'follow', 
            referrer: 'no-referrer', 
            body: JSON.stringify({
                "specifications": ["AS/NZS 2442.2:2000/Amdt 2:2007 (Legacy)",
                    "ASKO", 8, true, "Timer", "Slovenia", 890, 650, 200, "Heat and dry", 230, "Vented", 650]
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
                        <br />
                        <input
                            type='text'
                            placeholder='Appliance Standard'
                            value={this.state.applianceStandard}
                            onChange={this.handleChange}
                        />
                    </label>
                    <br />

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
