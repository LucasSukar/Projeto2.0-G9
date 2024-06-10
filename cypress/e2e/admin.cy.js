describe('admin', () => {
    it('admin', () => {
        cy.visit("/");
        cy.get('.column-left > a > .button').click();
        cy.get('#is_admin').select('Café');
        cy.get('#username').type("castro");
        cy.get('#password').type("andre");
        cy.get('.btn').click();
        cy.get('#id_username').type("castro");
        cy.get('#id_password').type("andre");
        cy.get('.btn').click();
        cy.get(':nth-child(4) > a > .bx').click();
        cy.get('#nome').type("Versado");
        cy.get('#endereco').type("Recife Antigo");
        cy.get('#cntt').type("81999998181");
        cy.get('#caracteristicas').type("tem wifi, calmo, bom");
        cy.get('.btn').click();
        cy.get(':nth-child(3) > a > .bx').click();
        cy.get('.list-group-item > :nth-child(1) > div').invoke('text').should('have.string', 'Versado na Recife Antigo (81999998181)');
        cy.get('#cafeteriadetail').click();
        cy.get('#edit').click();
        cy.get('#caracteristicas').clear();
        cy.get('#caracteristicas').type("tem wifi, calmo");
        cy.get('.btn').click();
        cy.get(':nth-child(3) > a > .bx').click();
        cy.get('.list-group-item').click();
        cy.get('.btn-success').click();
        cy.get('#novidade_texto').type("Promoção do dia: tudo 2 reais");
        cy.get('.btn-primary').click();
        cy.get('h6.card-text').invoke('text').should('have.string', 'Promoção do dia: tudo 2 reais');
        cy.get('.btn-sm').click();
        cy.get('.modal-footer > .btn-danger').click();
        cy.get(':nth-child(3) > .card > .card-body > p').invoke('text').should('have.string', 'Ainda não há novidades.');
        cy.get('.col-md-8 > .btn-danger').click();
        cy.get('.btn-secondary').click();
    })
})