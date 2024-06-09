describe('test suite Favoritar Cafeteria', () => {
    it('Favoritar a Cafeteria de Outra Pessoa', () => {
        cy.visit("/");
        cy.get('.column-left > a > .button').click();
        cy.get('#is_admin').select("cafe");
        cy.get('#username').type('cafe3');
        cy.get('#email').type('cafe3@gmail.com');
        cy.get('#password').type('XD123');
        cy.get('.btn').click();
        cy.get('#id_username').type('cafe3');
        cy.get('#id_password').type('XD123');
        cy.get('.btn').click();
        cy.get(':nth-child(4) > a > .bx').click();
        cy.get('#nome').type('Cafe n3');
        cy.get('#endereco').type('Rua 3');
        cy.get('#cntt').type('333333333');
        cy.get('#caracteristicas').type('Somos O Cafe n3');
        cy.get('.btn').click();
        cy.get(':nth-child(3) > a > .bx').click();
        cy.get('.logout > a > .bx').click();
        cy.get('.btn-secondary').click();
        cy.get('#username').type('Usuario3.3');
        cy.get('#email').type('Usuario3.3@gmail.com');
        cy.get('#password').type('XD123');
        cy.get('.btn').click();
        cy.get('#id_username').type('Usuario3.3');
        cy.get('#id_password').type('XD123');
        cy.get('.btn').click();
        cy.get(':nth-child(3) > a > .bx').click();
        cy.get('.list-group-item > :nth-child(1) > div').click();
        cy.get('#favBtn').click();
        cy.get(':nth-child(3) > a > .bx').click();






        //Deletar Alterções
        cy.get('.logout > a > .bx').click();
        cy.visit("/admin");
        cy.get('#id_username').type('admin');
        cy.get('#id_password').type('123');
        cy.get('.submit-row > input').click();
        cy.get('.model-user > th > a').click();
        cy.get(':nth-child(1) > .field-username > a').click();
        cy.get('.deletelink').click();
        cy.get('div > [type="submit"]').click();
        cy.get(':nth-child(2) > .field-username > a').click();
        cy.get('.deletelink').click();
        cy.get('div > [type="submit"]').click();
        cy.visit("/");
    })
})