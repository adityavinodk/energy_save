import React, { Component } from 'react'

class Response extends Component {
  componentDidMount () {
    if (this.props.response.category === 0) {
      document.getElementById('inference').classList.add('text-danger')
    }
    if (this.props.response.category === 1) {
      document.getElementById('inference').classList.add('text-info')
    }
    if (this.props.response.category === 2) {
      document.getElementById('inference').classList.add('text-success')
    }
  }

  render () {
    const links = this.props.response.links
    const listItems = links.map(link => (
      <li className='list-group-item'>
        <a href={link}>{link}</a>
      </li>
    ))

    const tableRows = Object.keys(this.props.response.correlatedParameters).map(
      parameter => (
        <tr>
          <td>{parameter}</td>
          <td>{this.props.response.correlatedParameters[parameter].join()}</td>
        </tr>
      )
    )
    return (
      <div className='row'>
        <div className='col-3' />
        <div className='card col-6 mx-0 px-0'>
          <div id='header' className='card-header h2'>
            Energy<label className='h1 text-success'>Save</label> Report
          </div>
          <div id='body' className='card-body'>
            <div id='category' className='card-title h3'>
              Category {this.props.response.category}
            </div>
            <div id='star_range' className='card-subtitle small font-bold'>
              (Range {this.props.response.starRange})
            </div>
            <div id='info' className='lead mb-3'>
              {this.props.response.info}
            </div>
            <div id='inference' className='font-italic mb-4 text-info'>
              {this.props.response.inference}
            </div>
            <hr class='my-4' />

            {Object.keys(this.props.response.correlatedParameters).length !==
            0 ? (
              <React.Fragment>
                  <label className='lead'>
                  Range of values for Category {this.props.response.category}
                </label>
                  <table class='table mb-1'>
                  <thead class='thead-dark'>
                      <tr>
                      <th scope='col'>Parameter</th>
                      <th scope='col'>Range</th>
                    </tr>
                    </thead>
                  <tbody>{tableRows}</tbody>
                </table>
                  {this.props.response.category === 2 ? null : (
                  <label className='small text-info font-italic mt-0 mb-4'>
                    If these parameters are dealt with, you can achieve a
                    reduction of{' '}
                      {this.props.response.idealEnergy[1] -
                      this.props.response.idealEnergy[0]}{' '}
                    kW/Hr
                    </label>
                  )}
                  <hr class='my-4' />
                </React.Fragment>
              ) : null}

            <div id='links'>
              <label className='h4'>Helpful Links</label>
              <ul className='list-group'>{listItems}</ul>
            </div>
          </div>
          <div id='footer' className='card-footer'>
            <button
              className='btn btn-success'
              onClick={() => {
                window.location.href = this.props.appliance
              }}
            >
              Fill Details Again
            </button>
          </div>
        </div>
      </div>
    )
  }
}

export default Response
