import React, { Component } from 'react'

class Home extends Component {
  constructor () {
    super()
    this.state = {
      appliance: ''
    }
    this.handleChange = this.handleChange.bind(this)
    this.selectAppliance = this.selectAppliance.bind(this)
  }
  handleChange (event) {
    this.setState({ appliance: event.target.value })
  }
  selectAppliance (e) {
    e.preventDefault()
    this.props.history.push('/' + this.state.appliance)
  }
  render () {
    return (
      <div className='container'>
        <div className='container-fluid'>
          <div className='h4 text-justify'>
            <label className='h2'>Energy</label>
            <label className='h1 text-success'>Save</label> helps to find the
            areas of high energy consumption in households based on predicting
            the health of the appliances
          </div>
          <div className='lead text-justify mb-3'>
            Our prediction models accurately predict the star rating of the
            appliances, old or new, with a number of features, and present a
            number of valuable insights on the ways of reducing the wastage
          </div>
        </div>
        <div className='jumbotron text-center'>
          <div className='display-4'>Let's Get Started</div>
          <div className='form-group'>
            <select
              className='form-control form-control-lg'
              value={this.state.appliance}
              onChange={this.handleChange}
            >
              <option value='' hidden>
                Select an Appliance
              </option>
              <option value='dryer'>Dryer</option>
              <option value='monitor'>Monitor</option>
              <option value='washing_machine'>Washing Machine</option>
            </select>
          </div>
          <input
            type='submit'
            value='Select'
            className='btn btn-lg btn-success w-25'
            onClick={this.selectAppliance}
          />
        </div>
      </div>
    )
  }
}

export default Home
