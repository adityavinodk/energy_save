import React, { Component } from 'react'

class Home extends Component {
    constructor() {
        super()
        this.state = {
            'appliance': ''
        }
        this.handleChange = this.handleChange.bind(this);
        this.selectAppliance = this.selectAppliance.bind(this);
    }
    handleChange(event) {
        this.setState({ 'appliance': event.target.value });
    }
    selectAppliance(e) {
        e.preventDefault();
        this.props.history.push('/dryer')
        // if (this.state.appliance === 'dryer') {
        //     return <Redirect to="/dryer" />
        // }

    }
    render() {
        return (
            <div className="container">
                <div className="jumbotron text-center">
                    <h1>Lets Get Started</h1>
                    <p>Select an Appliance</p>

                    <div className="form-group">
                            <select className="form-control form-control-lg" id="appliance">
                                <option value="dryer">Dryer</option>
                            </select>
                    </div>
                    <input type="submit" value="Select" className="btn btn-lg btn-success w-25" onClick={this.selectAppliance} />


                </div>
            </div>
        )
    }
}

export default Home


