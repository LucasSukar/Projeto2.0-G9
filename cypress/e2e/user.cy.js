describe('admin', () => {
    it('adicionar cafeteria', () => {
        cy.visit("/")
        cy.get('.column-left > a > .button').click()
        cy.get('#username').type("miguel")
        cy.get('#password').type("becker")
        cy.get('.btn').click()
        cy.get('#id_username').type("miguel")
        cy.get('#id_password').type("becker")
        cy.get('.btn').click()
    })
})