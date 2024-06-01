describe('test suite Adicionar Cafeteria', () => {
    it('Adicionar Cafeteria e Visualizar ela na Lista', () => {
        cy.visit("/");
        cy.get('.column-left > a > .button').click();
        cy.get('#is_admin').select("cafe");
        cy.get('#username').type('cafe1');
        cy.get('#email').type('cafe1@gmail.com');
        cy.get('#password').type('XD123');
        cy.get('.btn').click();
        cy.get('#id_username').type('cafe1');
        cy.get('#id_password').type('XD123');
        cy.get('.btn').click();
        cy.get(':nth-child(4) > a > .bx').click();
        cy.get('#nome').type('Cafe n1');
        cy.get('#endereco').type('Rua 1');
        cy.get('#cntt').type('111111111');
        cy.get('#caracteristicas').type('Somos O Cafe n1');
        cy.get('.btn').click();
        cy.get(':nth-child(3) > a > .bx').click();
    })
})
